import openai
from dotenv import load_dotenv
import logging
import os
import config

load_dotenv()

client = openai.OpenAI(api_key=config.api_key)
model = "gpt-4o"
assistant_id = config.assistant_id
thread_id = config.thread_id


def upload_file_to_openai(file, save_directory):

    try:
        save_path = os.path.join(save_directory, file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        # Create a vector store
        vector_store = client.beta.vector_stores.create(name="Uploaded Files Store")
        global vector_store_id
        vector_store_id = vector_store.id
        # Ready the files for upload to OpenAI
        file_stream = [file]

        # Upload the files and add them to the vector store
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_stream
        )

        # Print the status and the file counts of the batch
        print(file_batch.status)
        print(file_batch.file_counts)

        # Update the assistant to use the new Vector Store
        # assistant = client.beta.assistants.update(
        #    assistant_id=assistant_id,
        #    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        # )

        return "File uploaded successfully and assistant updated."

    except Exception as e:
        logging.error(f"An error occurred while uploading the file: {e}")
        return None


def delete_file(file_path, vector_store_id):
    try:
        # Supprimer le fichier du système de fichiers
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been deleted from the filesystem.")
        else:
            print(f"File {file_path} does not exist in the filesystem.")

        # Récupérer l'ID du fichier dans le vecteur de stockage
        files_in_store = client.beta.vector_stores.files.list(vector_store_id)
        file_to_delete = next(
            (file for file in files_in_store if file.file_path == file_path), None
        )

        if file_to_delete:
            # Supprimer le fichier du vecteur de stockage
            client.beta.vector_stores.files.delete(vector_store_id, file_to_delete.id)
            print(f"File {file_path} has been deleted from the vector store.")
        else:
            print(f"File {file_path} does not exist in the vector store.")

    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")
