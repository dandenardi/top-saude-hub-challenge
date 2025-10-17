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

export const OrderItemSchema = z.object({
  product_id: z.number().int().positive(),
  quantity: z.number().int().min(1, "Quantidade mínima é 1"),
});

export const OrderCreateSchema = z.object({
  customer_id: z
    .number({ invalid_type_error: "Informe um ID numérico" })
    .int()
    .positive("Cliente obrigatório"),
  items: z.array(OrderItemSchema).min(1, "Adicione pelo menos um item"),
});

export type OrderCreateInput = z.infer<typeof OrderCreateSchema>;
