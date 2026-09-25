# Tejas's demo guide

## The 20-second explanation

“I built an evidence investigation workbench for business onboarding. It helps an analyst match company names, inspect corporate relationships against their sources, and identify what still needs review. The model assists name matching; ownership claims remain grounded in documents.”

## Show it in three minutes

1. Start with Microsoft. Explain that Microsoft is a real public-record subject; Aster Pay is a fictional payments company used to demonstrate the analyst's workflow. These are not claimed customer relationships.
2. Search `Linked In Corporation`. The trained matcher ranks LinkedIn Corporation above the other names in the case. Inspect the first result.
3. Show the filing excerpt and open the original source. Point out the deliberate limit: listed subsidiary does not mean the exhibit proves its immediate parent, ownership percentage or human owners.
4. Mark the evidence reviewed. Open Review & gaps and add a note about what additional evidence you would request. Export the brief.
5. Load Ownership-chain example and select Willow Services. 80% times 60% yields a 48% path, only because both percentages are explicit.
6. Add a document and paste `Northstar Commerce PLC owns 75% of Harbor Payments Ltd.`. The conflicting claim blocks the 48% result. Exclude the new claim after reviewing its source and the path becomes calculable again. Neither action automatically verifies a business.

## Who uses it, and what gets solved?

A business onboarding analyst at a payments provider needs to understand the legal businesses involved before progressing a case. Evidence can be scattered across filings, uploaded statements and spelling variations. This app collects candidates, preserves exact evidence, flags contradictions and produces a review brief. It reduces manual transcription and makes an investigation easier to inspect. No measured time-saving or fraud-reduction result is claimed.

## What is actually ML?

A logistic regression model learns how six name-comparison signals relate to synthetic match labels. The browser executes its exported coefficients. It ranks candidates but does not merge entities automatically. The training set and method are reproducible. Synthetic validation is a software/model-development check, not proof of real-world identity accuracy.

## Why no autonomous verification agent?

The source may not contain the answer. A system that invents a direct owner from a subsidiary list would be worse than a blank field. Deterministic relationship extraction and arithmetic are intentionally narrow; a language model could later propose candidates, but proposals would still need source attribution and analyst review.

## Be ready to answer

- **Is this Trulioo's product?** No. Independent exploration of a problem their public UBO materials describe.
- **Is it production-ready compliance software?** No. It is a working deployed portfolio product. Shared storage, audit history, access control, licensed data integrations, document authenticity and domain evaluation remain production work.
- **Where are the real outcomes?** Not available. There is no claimed fraud accuracy, onboarding lift or customer adoption.
- **Why these companies?** Publicly accessible, inspectable filings make the evidence defensible. They are demonstration subjects, not design partners.
- **What is the biggest ML limitation?** Generated data and lexical features do not cover aliases, multilingual names or distinct companies with similar names. Validate on labeled business-resolution cases, compare exact/fuzzy baselines, and split by corporate family before expanding scope.
- **What would you do next with a team?** Obtain licensed, representative documents and adjudicated entity pairs; measure retrieval recall and false links against baselines; evaluate extraction with source-span accuracy; add persistent case history and reviewer permissions. Add document intelligence only if it improves those measurements.

