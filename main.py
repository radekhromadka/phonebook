from elasticsearch import Elasticsearch

class Phonebook:
    def __init__(self):
        # Setup connection to the local database; properly, the API key would be stored in a key vault or at least in .env file but for the sake of this task, it is very naughtily stored as plaintext within the code
        self.es = Elasticsearch("http://localhost:9200/", api_key="<YOUR_API_KEY_HERE>")
        self.index_name = "phonebook"

        # If phonebook index doesn't exist, create it
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, mappings={
                "properties": {
                    "name": {"type": "keyword"},
                    "phone_number": {"type": "keyword"}
            }})

    def add_contact(self, name, phone_number) -> bool:
        # Function to add new contact with a phone number, 
        search_check = self.es.search(index=self.index_name, query={"bool": {"filter": {"term": {"phone_number": phone_number}}}})  
        if not search_check['hits']['hits']:
            self.es.index(index=self.index_name, body={"name": name, "phone_number": phone_number})
            print(f"Added {phone_number} to the phonebook")
            return True
        else:
            print(f"{phone_number} already exists in the phonebook")
            return False

    def search_contact(self, initials) -> list[str]:
        # Function to search existing contacts by name (or part of it), prints a list of dicts with name and number of all contacts which match the search criteria
        query = {"query": { "regexp": {"name": f"{initials}.*"}}}
        response = self.es.search(index=self.index_name, body=query)

        # Unpack Elasticsearch response and return a list of phone numbers
        results = response['hits']['hits']
        return [result['_source']["phone_number"] for result in results]

if __name__ == "__main__":
    # On run, initialise Phonebook class
    phonebook = Phonebook()

    # If there are no entries, add some mock data
    if not phonebook.search_contact(""):
        phonebook.add_contact("Alice Smith", "123456789")
        phonebook.add_contact("Bob Johnson", "098765432")
        phonebook.add_contact("Charlie Brown", "555555555")

    # Properly this would be done using argparse but given the size of a task, inputs are used as a simplification
    operation = input("What operation should be performed (options: 'add', 'search')?\n")
    if operation == "add":
        name = input("Name of the person:\n")
        phone_number = input("Phone number:\n")
        confirm = input(f"Are these correct? Name: {name}, Phone number: {phone_number}; Y/n ")
        
        if confirm == "Y":
            phonebook.add_contact(name, phone_number)
        else:
            print("Cancelled")

    elif operation == "search":
        search = input("Search name:\n")
        search_results = phonebook.search_contact(search)
        print(search_results)

    else:
        print("Unknown operation, available options are 'add' and 'search' without quotes")
