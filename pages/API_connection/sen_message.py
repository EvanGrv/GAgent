import re
import openai
from dotenv import load_dotenv
import logging
from openai import AssistantEventHandler
from typing_extensions import override
import config  # Importer le fichier de configuration

load_dotenv()

client = openai.OpenAI(api_key=config.api_key)
model = "gpt-4o-mini-2024-07-18"
# Lire assistant_id et thread_id depuis le fichier de configuration
assistant_id = config.assistant_id
thread_id = config.thread_id


def make_links_clickable(text):
    drive_pattern = re.compile(r"(https://drive\.google\.com/file/d/[^\s]+) ")
    text = drive_pattern.sub(r'<a href="\1" target="_blank">Cliquez ici</a>', text)

    url_pattern = re.compile(r"(https?://[^\s]+)")
    text = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', text)

    # Remplacer les liens non standard 【】 par des liens cliquables
    custom_link_pattern = re.compile(r"【([^】]+)】")
    text = custom_link_pattern.sub(r'<a href="\1" target="_blank">\1</a>', text)

    print(f"Transformed text with clickable links: {custom_link_pattern}")
    return text


def remove_japanese_parentheses(text):
    print(text)
    try:
        # Premier motif : supprimer les éléments encadrés par les parenthèses japonaises
        pattern_general = r"【[^】]*】"
        cleaned_text = re.sub(pattern_general, "", text)

        # Deuxième motif : supprimer les éléments correspondant au motif spécifique
        pattern_specific = r"【\d+†source】"
        cleaned_text = re.sub(pattern_specific, "", cleaned_text)

        pattern_specific2 = "【.*?†source】"
        cleaned_text = re.sub(pattern_specific2, "", cleaned_text)

        return cleaned_text
    except Exception as e:
        print(f"An error occurred: {e}")
    return text


class EventHandler(AssistantEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.last_text = ""  # Stocker le dernier texte envoyé pour éviter les doublons

    @override
    def on_text_created(self, text_obj) -> None:
        text = text_obj.value if hasattr(text_obj, "value") else text_obj
        cleaned_text = remove_japanese_parentheses(text)
        transformed_text = make_links_clickable(cleaned_text)

        # Vérifier et enlever la répétition du premier mot
        transformed_text = self.remove_repeated_first_word(transformed_text)

        # Vérifier que le texte n'est pas vide et qu'il est différent du dernier envoyé
        if transformed_text and transformed_text != self.last_text:
            self.callback(transformed_text)
            self.last_text = transformed_text

    @override
    def on_text_delta(self, delta, snapshot):
        text = delta.value if hasattr(delta, "value") else delta
        cleaned_text = remove_japanese_parentheses(text)
        transformed_text = make_links_clickable(cleaned_text)

        # Vérifier et enlever la répétition du premier mot
        transformed_text = self.remove_repeated_first_word(transformed_text)

        # Vérifier que le texte n'est pas vide et qu'il est différent du dernier envoyé
        if transformed_text and transformed_text != self.last_text:
            self.callback(transformed_text)
            self.last_text = transformed_text

    def remove_repeated_first_word(self, text):
        # Vérifier si le texte commence par une répétition du premier mot
        words = text.split(maxsplit=2)  # Séparer les deux premiers mots uniquement
        if len(words) > 1 and words[0] == words[1]:
            # Si les deux premiers mots sont identiques, les supprimer une fois
            return text[
                   len(words[0]):].lstrip()  # Enlever seulement la première occurrence du mot en gardant les espaces
        return text
    def on_tool_call_created(self, tool_call):
        if (
            tool_call.type != "file_search"
        ):  # Exclude "file_search" from being displayed
            self.callback(f"\ncentre services> {tool_call.type}\n")

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                cleaned_input = remove_japanese_parentheses(
                    delta.code_interpreter.input
                )
                transformed_text = make_links_clickable(cleaned_input)
                self.callback(transformed_text)


def stop_active_runs(client, thread_id):
    try:
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        for run in runs.data:
            if run.status == "active":
                client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run.id)
    except Exception as e:
        logging.error(
            f"Une erreur s'est produite lors de l'arrêt des exécutions actives : {e}"
        )


def send_message_stream(message, callback):
    stop_active_runs(client, thread_id)
    event_handler = EventHandler(callback)

    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=message
    )

    try:
        with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler,
        ) as stream:
            stream.until_done()
    except Exception as e:
        logging.error(f"Une erreur s'est produite lors du flux de messages : {e}")


