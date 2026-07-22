from assistant.react.leader_agent import LeaderAgent

def main():
    print(f"--- Terraform oncall Agent open ---")
    config = {"configurable": {"thread_id": "default_thread_id", "user_id": "user_test_1"}}

    agent = LeaderAgent(config)

    agent.deal_question()

    print(f"--- Terraform oncall Agent close ---")

if __name__ == "__main__":
    main()