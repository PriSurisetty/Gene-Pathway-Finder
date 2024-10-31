from selenium import webdriver
from selenium.webdriver.common.by import By
import time

gene_name = input("\nPlease enter the name of the protein you want to retrieve the pathways for (e.g. AKAP9): ")

if gene_name:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.ebi.ac.uk/gwas/home")

    search_box = driver.find_element(By.ID, "search-box")
    search_box.send_keys(gene_name)
    driver.find_element(By.XPATH, "//*[@id='search-button']").click()

    time.sleep(1)

    results_container = driver.find_element(By.CLASS_NAME, "col-md-9")
    links = results_container.find_elements(By.TAG_NAME, "a")

    gene_found = False
    for link in links:
        if gene_name in link.text:
            link.click()
            gene_found = True
            break

    if not gene_found:
        print("\nGene not found.")
        driver.quit()
        exit()

    time.sleep(1)

    locate_pi = driver.find_element(By.CLASS_NAME, "row")
    click_pi = locate_pi.find_element(By.ID, "ensembl_pathway_button")
    click_pi.click()

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(5)  # Give extra time for the pathways page to load

    pathways_list = driver.find_elements(By.CLASS_NAME, "pathways_list")
    if pathways_list:
        for pathways in pathways_list:
            items = pathways.find_elements(By.TAG_NAME, "li")
            print(f"\nList of pathways for the {gene_name} gene:\n")
            for item in items:
                # Extract the text from the <i> tag inside each <li>
                pathway_name = item.find_element(By.TAG_NAME, "i").text
                print(f'~ {pathway_name}')  # Print just the pathway name
    else:
        print("\nNot found.")

    driver.quit()
