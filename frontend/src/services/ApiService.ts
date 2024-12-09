export class ApiService {
  private static instance: ApiService | null = null;
  private ENDPOINT: string = import.meta.env.VITE_END_POINT;

  private constructor() {}

  public static getInstance(): ApiService {
    if (!this.instance) {
      this.instance = new ApiService();
    }
    return this.instance;
  }

  /**
   * fetch http get method
   * @param path
   */
  async get<T>(path: string): Promise<T | null> {
    const url = `${this.ENDPOINT}/${path}`;

    try {
      const response = await fetch(url, {
        method: "GET",
        headers: this.header(),
      });

      if (!response.ok) {
        console.log(`fetch error: ${url}`);
        console.log(response);
        return null;
      }

      const data: T = await response.json();
      return data;
    } catch (e) {
      console.log(e);
      return null;
    }
  }

  /**
   * fetch http post method
   * @param path
   * @param body
   */
  async post<T, V>(path: string, body: V): Promise<T | null> {
    const url = `${this.ENDPOINT}/${path}`;

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: this.header(),
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        console.log(`fetch error: ${url}`);
        console.log(response);
        return null;
      }

      const data: T = await response.json();
      return data;
    } catch (e) {
      console.log(e);
      return null;
    }
  }

  private header() {
    const header = new Headers();
    header.append("Content-Type", "application/json");
    return header;
  }
}
