import { ApiError } from "@/lib/api-error";
import { api } from "@/lib/api";

describe("apiFetch envelope handling", () => {
  const originalFetch = global.fetch as any;
  let dispatchSpy: jest.SpyInstance;

  beforeEach(() => {
    global.fetch = jest.fn() as any;

    dispatchSpy = jest
      .spyOn(window, "dispatchEvent")
      .mockImplementation(() => true);
  });

  afterEach(() => {
    global.fetch = originalFetch;
    dispatchSpy.mockRestore();
    jest.clearAllMocks();
  });

  it("retorna data quando cod_retorno = 0", async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({ cod_retorno: 0, mensagem: null, data: [{ id: 1 }] }),
    });

    const rows = await api.products.list();
    expect(rows).toEqual([{ id: 1 }]);
    expect(dispatchSpy).not.toHaveBeenCalled();
  });

  it("lança ApiError e emite evento quando cod_retorno = 1", async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({ cod_retorno: 1, mensagem: "Falha", data: null }),
    });

    await expect(api.products.list()).rejects.toBeInstanceOf(ApiError);

    expect(dispatchSpy).toHaveBeenCalledTimes(1);
    const evt = dispatchSpy.mock.calls[0][0] as CustomEvent;
    expect(evt.type).toBe("api-error");
    expect((evt as any).detail).toBe("Falha");
  });

  it("lança ApiError com status quando HTTP != 2xx sem envelope", async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      status: 500,

      json: async () => {
        throw new Error("no json");
      },
      clone: () => ({ text: async () => "Erro interno" }),
    });

    await expect(api.products.list()).rejects.toBeInstanceOf(ApiError);
    expect(dispatchSpy).toHaveBeenCalled();
  });
});
