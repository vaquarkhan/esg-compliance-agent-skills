# GHG inventory example

Runnable end-to-end inventory from activity CSV → JSON with factor provenance.

```bash
python examples/ghg-inventory/run_inventory.py
```

Outputs:

- `examples/ghg-inventory/ghg_inventory.json`
- `examples/ghg-inventory/factor_provenance.json`

Uses real MCP server logic against `knowledge_base/emission_factors.json`. Human review required before external disclosure.
