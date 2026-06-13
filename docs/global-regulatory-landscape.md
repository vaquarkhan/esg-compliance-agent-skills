# Global regulatory landscape — APAC, LATAM, MENA

ISSB S1/S2 is the converging baseline across regions, with jurisdiction-specific overlays and localization constraints.

## Asia-Pacific

| Jurisdiction | Framework | Mandatory timeline | Language | Localization |
| --- | --- | --- | --- | --- |
| Singapore (SGX) | ISSB-aligned climate | FY2025 large-cap; FY2027 all listed | English | PDPA |
| Australia (ASRS) | AASB climate standards | Jan 2025 Group 1 (>$500M revenue); Jul 2026 Group 2; Jul 2027 Group 3 | English | Privacy Act |
| Japan (SSBJ) | IFRS S1/S2 adoption | FY2027 Prime Market large caps | Japanese | APPI |
| India (BRSR Core) | SEBI BRSR | Top 1,000 listed; assurance phased top 150 → 1,000 by FY2027 | English | **DPDP Act 2023** |
| South Korea (KSSB) | KSSB standards | 2027 (>2T KRW assets) | Korean / English | PIPA |

**India overlay:** caste diversity, MSE procurement (BRSR-specific social indicators).

## Latin America

| Jurisdiction | Framework | Mandatory timeline | Language |
| --- | --- | --- | --- |
| Brazil (CVM Res. 193) | ISSB S1/S2 aligned | FY2026 reports due 2027 | **Portuguese** |
| Mexico (BMV) | Voluntary TCFD/GRI | No confirmed mandatory date | Spanish / English |

## Middle East / North Africa

| Jurisdiction | Framework | Mandatory timeline | Language | Localization |
| --- | --- | --- | --- | --- |
| UAE (SCA) | ESG Disclosure Framework | FY2024 ADX/DFM listed | English / Arabic | UAE Net Zero 2050 overlay |
| Saudi Arabia (Tadawul) | ESG Disclosure Guidelines | 2025 large-cap; 2027 all listed | **Arabic** / English | **PDPL** + Vision 2030 KPIs |

## Cross-border architecture constraints

Before routing ESG data across regions:

1. Load Skill 10 (`cross-border-data-transfer`)
2. Consult `knowledge_base/jurisdiction_reporting.json`
3. Enforce DPDP (India), PIPL (China), PDPL (Saudi) residency rules
4. Match filing language to jurisdiction (JP/BR/SA official filings)

Machine-readable stubs: [knowledge_base/jurisdiction_reporting.json](../knowledge_base/jurisdiction_reporting.json).
