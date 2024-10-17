import { RemoteRunnable } from "@langchain/core/runnables/remote";

const pyAssistant = async (question: string): Promise<string> => {
  const chain = new RemoteRunnable({
    url: `http://localhost:8000/rag`,
  });
  
  try {
    const result = await chain.invoke(question);
    return result as string;
  } catch (error) {
    console.error("Error fetching:", error);
    throw error;
  }
};

export default pyAssistant;