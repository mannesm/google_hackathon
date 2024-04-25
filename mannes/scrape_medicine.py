from typing import Tuple, Dict

import requests
from bs4 import BeautifulSoup as Soup


def basic_scraper(medication_name: str) -> tuple[str, str, str]:
    """Scrapes side effects and dosage information for a given medication from farmacotherapeutischkompas.nl.

    Args:
        medication_name (str): The name of the medication to scrape.

    Returns:
        tuple[str, str]: A tuple containing the side effects and dosage information, respectively.
               Returns ('No medication details found', 'No medication details found') if any exception occurs.
    """
    url = f"https://www.farmacotherapeutischkompas.nl/bladeren/preparaatteksten/{medication_name[0].lower()}/{medication_name}/"
    try:
        # Fetch the HTML content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors

        # Parse the HTML content
        soup = Soup(response.text, 'html.parser')

        bijwerkingen_section = soup.find('section', id="bijwerkingen")
        bijwerkingen_text = bijwerkingen_section.get_text(separator="\n", strip=True)

        # Extract "doseringen" section
        doseringen_section = soup.find('section', id="doseringen")
        doseringen_text = doseringen_section.get_text(separator="\n", strip=True)

        return bijwerkingen_text, doseringen_text, url
    except requests.exceptions.RequestException as err:
        print("Oops! Something went wrong:", err)
        return 'No medication details found', 'No medication details found', 'No URL found'  # Return an empty tuple on any exception


def scrape_medications(medicine_list: Dict[str, list]) -> Dict[str, Dict[str, str]]:
    """Scrapes side effects and dosage information for a list of medications.

    Args:
        medicine_list (Dict[str, list]): A dictionary where the key is "medicijnen" and the value is a list of medication names.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where keys are medication names and values are dictionaries containing "bijwerkingen" (side effects) and "dosering" (dosage) information.
    """
    bijwerkingen_dosering = {}
    for medicine in medicine_list:
        bijwerking, dosering, url = basic_scraper(medicine.lower())
        bijwerkingen_dosering[medicine] = {"bijwerkingen": bijwerking, "dosering": dosering, "url": url}

    return bijwerkingen_dosering


# Example usage:
medicine_list = ["buPROPion", "clonazePAM", "clotrimazole", "cyanocobalamin", "cyclobenzaprine", "diclofenac", "etodolac", "famotidine", "FLUoxetine", "gabapentin", "hydrocortisone", "levocarnitine", "lidocaine-diphenhydrAMINE-maalox", "lipase-protease-amylase", "LORazepam", "montelukast", "multivitamin", "rOPINIRole", "tamsulosin", "thyroid", "zolpidem", "Tylenol", "Flexeril"]


results = scrape_medications(medicine_list)
