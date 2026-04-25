import re
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from ..bot import automation


def _digits(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def _best_effort_store_lookup(self: "automation", raw: str, digits: str) -> Dict[str, Optional[str]]:
    script = r"""
        const raw = (arguments[0] || "").trim();
        const rawLower = raw.toLowerCase();
        const onlyDigits = (arguments[1] || "").trim();
        const out = { nome: null, jid: null, lid: null, numero: null };

        const normalizeDigits = (v) => (v || "").replace(/\D/g, "");
        const toNumber = (user) => user && /^\d+$/.test(user) ? `+${user}` : null;
        const toSerialized = (idObj) => (idObj && (idObj._serialized || idObj.id || "") || "").toString();

        const fillFromId = (serialized, name) => {
            if (!serialized) return false;
            if (serialized.endsWith("@lid")) out.lid = serialized;
            else out.jid = serialized;
            const user = serialized.split("@", 1)[0];
            if (user && /^\d+$/.test(user)) out.numero = `+${user}`;
            if (name) out.nome = name;
            return true;
        };

        const ensureStore = () => {
            // 1) Já exposto (compatível com algumas builds)
            if (window.Store && window.Store.Chat) return window.Store;
            if (window.WWebJS && window.WWebJS.Store && window.WWebJS.Store.Chat) return window.WWebJS.Store;

            // 2) Tenta localizar objeto global com Chat/Contact
            for (const key of Object.keys(window)) {
                try {
                    const v = window[key];
                    if (v && v.Chat && v.Contact) {
                        window.Store = v;
                        return window.Store;
                    }
                } catch (_) {}
            }
            return null;
        };

        try {
            const store = ensureStore();
            const chats = (store && store.Chat && store.Chat.models) || [];

            for (const chat of chats) {
                const idObj = chat.id || chat.__x_id || {};
                const serialized = toSerialized(idObj);
                const user = (idObj.user || "").toString();
                const server = (idObj.server || "").toString();
                const number = toNumber(user);
                const name = (
                    chat.name ||
                    chat.formattedTitle ||
                    (chat.contact && (chat.contact.name || chat.contact.formattedName)) ||
                    ""
                ).toString().trim();

                const isMatchByName = name && name.toLowerCase() === rawLower;
                const isMatchById = serialized && serialized.toLowerCase() === rawLower;
                const isMatchByDigits = number && onlyDigits && normalizeDigits(number) === onlyDigits;

                if (!(isMatchByName || isMatchById || isMatchByDigits)) continue;

                out.nome = name || null;
                out.numero = number || null;
                fillFromId(serialized, name || null);
                return out;
            }
        } catch (_) {}

        // 3) Fallback: tenta chat ativo (quando conversa já está aberta)
        try {
            const store = ensureStore();
            let active = null;
            if (store && store.Chat && typeof store.Chat.getActive === "function") {
                active = store.Chat.getActive();
            } else if (store && store.Chat && store.Chat.models) {
                active = store.Chat.models.find(c => c && c.active);
            }

            if (active) {
                const idObj = active.id || active.__x_id || {};
                const serialized = toSerialized(idObj);
                const name = (
                    active.name ||
                    active.formattedTitle ||
                    (active.contact && (active.contact.name || active.contact.formattedName)) ||
                    ""
                ).toString().trim();

                const number = toNumber((idObj.user || "").toString());
                const activeMatchesRaw =
                    (name && name.toLowerCase() === rawLower) ||
                    (serialized && serialized.toLowerCase() === rawLower) ||
                    (number && onlyDigits && normalizeDigits(number) === onlyDigits);

                if (activeMatchesRaw || (!raw && (name || serialized))) {
                    out.nome = out.nome || name || null;
                    out.numero = out.numero || number || null;
                    fillFromId(serialized, name || null);
                    return out;
                }
            }
        } catch (_) {}

        return out;
    """
    try:
        return self.driver.execute_script(script, raw, digits) or {
            "nome": None,
            "jid": None,
            "lid": None,
            "numero": None,
        }
    except Exception:
        return {
            "nome": None,
            "jid": None,
            "lid": None,
            "numero": None,
        }


def identificar_contato(self: "automation", identificador: str) -> Dict[str, Optional[str]]:
    raw = (identificador or "").strip()
    only_digits = _digits(raw)

    info: Dict[str, Optional[str]] = {
        "input": raw,
        "tipo": None,
        "nome": None,
        "jid": None,
        "lid": None,
        "numero": None,
    }

    if not raw:
        info["tipo"] = "invalido"
        return info

    lower = raw.lower()
    if lower.endswith("@lid"):
        info["tipo"] = "lid"
        info["lid"] = raw
        user = raw.split("@", 1)[0]
        if user.isdigit():
            info["numero"] = f"+{user}"
    elif "@c.us" in lower or "@s.whatsapp.net" in lower:
        info["tipo"] = "jid"
        info["jid"] = raw
        user = raw.split("@", 1)[0]
        if user.isdigit():
            info["numero"] = f"+{user}"
    elif only_digits:
        info["tipo"] = "numero"
        info["numero"] = f"+{only_digits}"
        info["jid"] = f"{only_digits}@c.us"
    else:
        info["tipo"] = "nome"
        info["nome"] = raw

    # lookup best-effort no Store para enriquecer jid/lid/nome/numero
    enriched = _best_effort_store_lookup(self, raw, only_digits)
    info["nome"] = info["nome"] or enriched.get("nome")
    info["jid"] = info["jid"] or enriched.get("jid")
    info["lid"] = info["lid"] or enriched.get("lid")
    info["numero"] = info["numero"] or enriched.get("numero")

    return info
