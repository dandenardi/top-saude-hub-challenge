import { z } from "zod";

export const productSchema = z.object({
  name: z.string().min(1, "Nome é obrigatório"),
  sku: z
    .string()
    .trim()
    .min(1, "SKU é obrigatório")
    .regex(/^\S+$/, "Sem espaços"),
  price: z.coerce.number().int().positive("Preço deve ser > 0"),
  stock_qty: z.coerce.number().int().min(0, "Estoque não pode ser negativo"),
  is_active: z.boolean().optional().default(true),
});

export const customerSchema = z.object({
  name: z.string().min(1, "Nome é obrigatório"),
  email: z.string().email("E-mail inválido"),
  document: z.string().min(6, "Documento inválido"),
});
