import { verify } from "https://deno.land/x/djwt@v2.9.1/mod.ts";

async function _asyncverifyRequest(req: Request): Promise<boolean> {
    const webhooksPublicKey = Deno.env.get("WEBHOOKS_PUBLIC_KEY");
  
    if (!req.headers.has("X-Lago-Signature")) {
      return false;
    }
  
    const token = req.headers.get("X-Lago-Signature");
  
    const body = await req.json()
  
    const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(webhooksPublicKey!), {name: "RSASSA-PKCS1-v1_5", hash: "SHA-256"}, false, ["verify"]);
  
    const payload = await verify(token!, key);
  
    if (payload !== body) {
      return false;
    }
  
    return true;
  }