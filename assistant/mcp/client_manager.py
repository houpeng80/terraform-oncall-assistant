class MCPClientManager:
    async def list_tools(self, config):
        async with Client(config.source, timeout=config.timeout_seconds) as client:
            return await client.list_tools()

    async def call_tool(self, config, remote_name, arguments):
        async with Client(config.source, timeout=config.timeout_seconds) as client:
            return await client.call_tool(remote_name, arguments)

