# semantic-kernel-example-ChatGPT-Plugin
Microsoft Semantic Kernel - Example application creating ChatGPT plugin using Native and Semantic function with Python and Azure Function App. In this example code, we demonstrate how to combine native functions with semantic functions to correctly answer word problems like What is the "square root of 634?", "What is 42 plus 1513" or "multiply 2 times 4", etc.

## Microsoft Semantic Kernel

The [Microsoft Semantic kernel](https://learn.microsoft.com/en-us/semantic-kernel/ai-orchestration/kernel/?tabs=Csharp) is responsible for managing resources that are necessary to run "code" in an AI application. This includes managing the configuration, services, and plugins necessary for native code and AI services to run together.

Semantic Kernel makes it easy to run AI services alongside **native code** by treating calls to AI services as their first-class citizens called "semantic functions."

## AI Plugins

[AI Plugins](https://learn.microsoft.com/en-us/semantic-kernel/ai-orchestration/plugins/?tabs=Csharp) in Semantic Kernel are the fundamental building blocks of Semantic Kernel and can interoperate with plugins in ChatGPT, Bing, and Microsoft 365. With plugins, you can encapsulate capabilities into a single unit of functionality that the kernel can run. Plugins can consist of both **native code** and requests to AI services via **semantic functions**.

### Semantic Functions

Semantic Functions listen to users' asks and respond with a natural language response within your AI app. AI app operates very much like the human body; the Prompt represents "Ear", the Response as "Mouth", and the LLM model as "brain". Semantic Kernel uses connectors to connect the Prompt and the Response to the "brain". This allows you to easily swap out the AI services ("brain") without rewriting code.

### Native Functions

With Native Functions, you can have the Semantic kernel call C# or Python code directly so you can manipulate data or perform other operations, perform a task LLMs cannot do easily on their own. For example, you want to perform a task based on the intent that can be achieved using Semantic Functions. Now, if the user wants to send an email, you'll need to make the necessary API calls to send an email; this can be done using Native Functions.

## ChatGPT Plugin

The ChatGPT Plugin consists of three things: an app wrapped in an API, a manifest file, and an OpenAPI specification.

![alt](./images/MathSkill.png)

## Prerequisites

- [Azure Functions Core Tools](https://www.npmjs.com/package/azure-functions-core-tools)
- [VSCode](https://code.visualstudio.com/download)
- Python >= 3.10
- OpenAI API Key
