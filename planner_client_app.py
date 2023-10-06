"""instead of relying on our own OrchestratorPlugin to chain the MathPlugin and semnatic functions, we'll use planner to do it for us!"""

import asyncio
from semantic_kernel.planning.sequential_planner import SequentialPlanner

from semanticutil.kernel_utils import KernelUtil

async def main():
    """main function"""
    kernel =  KernelUtil.create_kernel_for_request()
    ask = "If my investment of 2130.23 dollars increased by 23, how much would I have after I spent $5 on a latte?"
    planner = SequentialPlanner(kernel)
    plan = await planner.create_plan_async(ask)
    # Execute the plan
    result = await kernel.run_async(plan)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())