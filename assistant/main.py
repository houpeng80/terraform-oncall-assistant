from assistant.react.leader_agent import LeaderAgent

def main():
    print(f"--- Terraform oncall Agent open ---")
    config = {"configurable": {"thread_id": "default_thread_id", "user_id": "default_user_id"}}

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["q", "quit"]:
            break

        LeaderAgent(config).react(user_input)

    print(f"--- Terraform oncall Agent close ---")

if __name__ == "__main__":
    main()