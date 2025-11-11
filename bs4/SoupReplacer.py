from typing import Optional, Callable, Dict, Any
class SoupReplacer:
    """
    1) Milestone-2
    Example: SoupReplacer(og_tag, alt_tag)
    
    2) Milestone-3
    Example: SoupReplacer(name_xformer=None, attrs_xformer=None, xformer=None)
    - name_xformer(tag) -> str         # return new tag name
    - attrs_xformer(tag) -> dict       # return new attributes dict
    - xformer(tag) -> None             # can mutate tag in-place (side effects)

    """
    def __init__(
        self,
        og_tag: Optional[str] = None,
        alt_tag: Optional[str] = None,
        *,
        name_xformer: Optional[Callable[[Any], str]] = None,
        attrs_xformer: Optional[Callable[[Any], Dict[str, Any]]] = None,
        xformer: Optional[Callable[[Any], None]] = None,
    ):
        # Back-compat path: positional (og_tag, alt_tag)
        self._legacy_og = (og_tag or "").lower() if og_tag is not None else None
        self._legacy_alt = (alt_tag or "").lower() if alt_tag is not None else None

        # New transformer functions
        self._name_xformer = name_xformer
        self._attrs_xformer = attrs_xformer
        self._xformer = xformer

        # If user used legacy positional API, synthesize a name_xformer so that
        # both .map_name() and .apply() share the same rule.
        if self._legacy_og is not None and self._legacy_alt is not None:
            if self._name_xformer is None:
                def _legacy_name_xformer(tag):
                    # tag may be a str (when called via map_name) or a Tag
                    name = tag if isinstance(tag, str) else getattr(tag, "name", "")
                    return self._legacy_alt if (name or "").lower() == self._legacy_og else name
                self._name_xformer = _legacy_name_xformer

    # ---------- Used by the builder before Tag creation ----------
    def map_name(self, name: str) -> str:
        # 沒有 name_xformer：維持舊行為（含 legacy M2）
        if self._name_xformer is None:
            if self._legacy_og is not None and self._legacy_alt is not None:
                return self._legacy_alt if (name or "").lower() == self._legacy_og else name
            return name

        # 先嘗試用 Tag-like 假物件呼叫（符合 lambda tag: ... 期望）
        class _TagShim:
            __slots__ = ("name", "attrs")
            def __init__(self, n):
                self.name = n
                self.attrs = {}

        try:
            new_name = self._name_xformer(_TagShim(name))
            if new_name:
                return new_name
        except Exception:
            pass

        # 失敗時再用原始字串重試（給能接受 str 的函式）
        try:
            new_name = self._name_xformer(name)
            if new_name:
                return new_name
        except Exception:
            pass

        return name


    # Backward-compat alias (your _htmlparser.py already calls rep.map(name))
    def map(self, name: str) -> str:
        return self.map_name(name)

    # ---------- Used by BeautifulSoup after Tag creation ----------
    def apply(self, tag) -> None:
        """
        Called AFTER the Tag object is constructed, but BEFORE it is pushed
        on the stack (so that downstream sees updated state).

        Order:
          1) name_xformer  -> tag.name (if provided)
          2) attrs_xformer -> tag.attrs (if provided)
          3) xformer       -> side effects (if provided)
        """
        # 1) name_xformer on real Tag
        if self._name_xformer is not None:
            try:
                new_name = self._name_xformer(tag)
                if new_name and new_name != tag.name:
                    tag.name = new_name
            except Exception:
                # Be robust: never break parsing due to a transformer
                pass

        # 2) attrs_xformer
        if self._attrs_xformer is not None:
            try:
                new_attrs = self._attrs_xformer(tag)
                if isinstance(new_attrs, dict):
                    tag.attrs = new_attrs
            except Exception:
                pass

        # 3) general xformer with side effects
        if self._xformer is not None:
            try:
                self._xformer(tag)
            except Exception:
                pass