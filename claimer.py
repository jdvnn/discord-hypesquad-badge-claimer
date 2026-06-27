import sys
import requests

class HypeSquadAPI:
    def __init__(self, token: str):
        self.endpoint = "https://discord.com/api/v9/hypesquad/online"
        self.headers = {
            "Authorization": token.strip(),
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        self.houses = {
            1: "Bravery",
            2: "Brilliance",
            3: "Balance"
        }

    def _make_request(self, method: str, payload=None):
        try:
            if method == "POST":
                response = requests.post(self.endpoint, headers=self.headers, json=payload)
            elif method == "DELETE":
                response = requests.delete(self.endpoint, headers=self.headers)
            else:
                return False, "Unsupported HTTP method."

            if response.ok:
                return True, "Success!"
            
            error_msg = response.json().get("message", "Unknown error") if response.content else response.text
            return False, f"Error {response.status_code}: {error_msg}"
            
        except requests.RequestException as e:
            return False, f"Connection error: {e}"

    def set_house(self, house_id: int):
        if house_id not in self.houses:
            return False, "Invalid house ID (must be between 1 and 3)."
        
        success, msg = self._make_request("POST", {"house_id": house_id})
        if success:
            return True, f"{self.houses[house_id]} badge successfully claimed!"
        return False, msg

    def remove_house(self):
        success, msg = self._make_request("DELETE")
        if success:
            return True, "Badge successfully removed."
        return False, msg


def main():
    print("Discord HypeSquad Badge Claimer")
    print("Developer: Jadven")
    print("-" * 60)

    token = input("Enter Discord Token: ").strip()
    if not token:
        print("Token cannot be empty.")
        sys.exit(1)

    api = HypeSquadAPI(token)

    while True:
        print("\nOptions:")
        print("1. Bravery Badge")
        print("2. Brilliance Badge")
        print("3. Balance Badge")
        print("4. Remove Badge")
        print("q. Quit")

        choice = input("\nYour choice (1-4 or q): ").strip().lower()

        if choice == "q":
            print("Exiting...")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please try again.")
            continue

        print()
        if choice == "4":
            success, msg = api.remove_house()
        else:
            success, msg = api.set_house(int(choice))

        print(msg)
        print("-" * 60)


if __name__ == "__main__":
    main()