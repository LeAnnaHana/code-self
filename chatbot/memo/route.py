from llama_index.core.selectors import LLMMultiSelector
from llama_index.core.tools import ToolMetadata

# Step 1: Create the selector
selector = LLMMultiSelector.from_defaults()
tool_choices = [
    ToolMetadata(
        name="general_chat",
        description="This handles general conversation and chitchat",
    ),
    ToolMetadata(
        name="product_info", 
        description="This handles questions about products, pricing, and availability",
    ),
]
def route(user_intent):
    # Select the best tool based on user intent
    selector_result = selector.select(tool_choices, query=user_intent)
    
    # Handle cases where no selection is made
    if not selector_result.selections:
        return "unknown"  
    
    # Get the selected tool metadata
    selected_tool = tool_choices[selector_result.selections[0].index]
    return selected_tool.name


user_query = "Can you tell me the price of this laptop?"
selected_route = route(user_query)
print(f"Selected Route: {selected_route}")
# Output: Selected Route: product_info
