import requests

from PIL import Image

from io import BytesIO

from config import HF_API_KEY


# Define the API endpoint as a constant

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"


def generate_image_from_text(prompt: str) -> Image.Image:

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {"inputs": prompt}


    try:

        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        response.raise_for_status()  # Raise an error for bad status codes


        # Check if the response content is an image

        if 'image' in response.headers.get('Content-Type', ''):

            image = Image.open(BytesIO(response.content))

            return image

        else:

            raise Exception("The response is not an image. It might be an error message.")

    except requests.exceptions.RequestException as e:

        raise Exception(f"Request failed: {e}")


def main():

    """

    Main loop for user interaction. Continuously prompts the user for a text description,

    generates an image via the API, displays it, and offers an option to save the image.

    """

    print("Welcome to the Text-to-Image Generator!")

    print("Type 'exit' to quit the program.\n")

   

    while True:

        prompt = input("Enter a description for the image you want to generate:\n").strip()

        if prompt.lower() == "exit":

            print("Goodbye!")

            break

       

        print("\nGenerating image...\n")

        try:

            image = generate_image_from_text(prompt)

            image.show()


            save_option = input("Do you want to save this image? (yes/no): ").strip().lower()

            if save_option == "yes":

                file_name = input("Enter a name for the image file (without extension): ").strip() or "generated_image"

                # Basic validation for file name

                file_name = "".join(c for c in file_name if c.isalnum() or c in ('_', '-')).rstrip()

                image.save(f"{file_name}.png")

                print(f"Image saved as {file_name}.png\n")

        except Exception as e:

            print(f"An error occurred: {e}\n")

       

        print("-" * 80 + "\n")


if __name__ == "__main__":

    main()