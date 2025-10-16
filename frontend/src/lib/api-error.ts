export class ApiError extends Error {
  constructor(public status: number, message?: string) {
    super(message);
    this.name = "ApiError";
  }
}

export async function parseJsonSafe(res: Response) {
  try {
    return await res.json();
  } catch (error) {
    console.error("Error parsing JSON: ", error);
    return null;
  }
}
