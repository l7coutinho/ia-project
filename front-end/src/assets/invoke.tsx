import { RemoteRunnable } from "@langchain/core/runnables/remote";

const pyAssistent = async (question: string) => {
  const chain = new RemoteRunnable({
    url: `http://localhost:8000/python/`,
  });

  try {
    const result: any = await chain.invoke({ question });
    return result.content;
  } catch (error) {
    console.error("Error fetching:", error);
    throw error;
  }
};

export default pyAssistent;
