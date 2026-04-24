# The Pets Table Plans Quiz - Strict Prototype

**Production-quality prototype matching the exact implementation from the web repo.**

## Overview

This prototype replicates The Pets Table's production plans-quiz flow, a 10-step onboarding questionnaire that collects pet profile information to generate personalized meal plans.

## How to Preview

Open the prototype in your browser:

```bash
open /Users/katreena.dalisay/Documents/spec-machine-prototypes/wellness-boosts-before-checkout-v2/index.html
```

Or simply double-click `index.html` in Finder.

## Quiz Flow (Production Implementation)

### Step 1: Number of Pets
- **Component**: `QuizNumberOfPets`
- **Input**: Segmented buttons (1, 2, 3, 4, 5+)
- **Output**: `numberOfPets`

### Step 2: Name & Sex
- **Component**: `QuizNameAndSex`
- **Inputs**: Radio buttons (Male/Female), Text input (name)
- **Outputs**: `sex`, `name`

### Step 3: Goals
- **Component**: `QuizGoal`
- **Input**: Radio cards (Maintain/Lose/Gain weight)
- **Output**: `goals`

### Step 4: Age
- **Component**: `QuizAge`
- **Inputs**: Two dropdowns (Years, Months)
- **Outputs**: `ageYears`, `ageMonths`

### Step 5: Breed
- **Component**: `QuizBreed`
- **Inputs**: Text input (breed search), Checkbox (unknown breed), Segmented buttons (size if unknown)
- **Outputs**: `breed`, `breedSize`, `unknownBreed`

### Step 6: Weight
- **Component**: `QuizWeight`
- **Input**: Number input (pounds)
- **Output**: `weightInLbs`

### Step 7: Body Condition
- **Component**: `QuizBodyConditions`
- **Input**: Radio cards (Underweight/Ideal/Overweight/Obese)
- **Output**: `bodyCondition`

### Step 8: Allergens
- **Component**: `QuizAllergens`
- **Inputs**: Checkboxes (Beef, Chicken, Fish, Dairy, Wheat, Corn, None)
- **Output**: `allergens` (array)

### Step 9: Activity Level
- **Component**: `QuizActivityLevel`
- **Input**: Radio cards (Low/Moderate/High activity)
- **Output**: `activityLevel`

### Step 10: Feeding Plan Type
- **Component**: `QuizFeedingPlanType`
- **Input**: Radio cards (100% Fresh / 50% Fresh + 50% Current / Air-Dried)
- **Output**: `feedingPlanType`

### Final: Calculating
- Loading screen with progress bar
- Transitions to plans selection (not implemented in this prototype)

## Implementation Details

### State Management
- Uses `localStorage` with namespaced keys via `ProtoStorage` utility
- Persists quiz progress and form data across page reloads
- User can navigate Back/Continue through steps

### Validation
- Each step validates required fields before allowing progression
- Error messages displayed inline matching production patterns
- Form state preserved when navigating between steps

### UI Patterns (Production Match)
- **Full-width footer bar** with Back/Continue buttons (production pattern)
- **Step badge** showing "Step X of 10" (production component)
- **Pet name interpolation** throughout the flow (personalization)
- **Radio size cards** for selections with descriptions (production component)
- **Segmented buttons** for numeric/category selections (production component)
- **Dropdowns** with custom styling (production pattern)

## Brand Tokens (The Pets Table)

- **Primary**: `#2E2E2E` (dark gray)
- **Accent**: `#BD0099` (magenta), `#007885` (teal)
- **Background**: `#F0F9F9` (light cyan)
- **Typography**: Poppins (headings), Source Sans 3 (body)
- **Border Radius**: `1rem` (rounded corners, brand characteristic)

## Source

- **Reference URL**: https://www.thepetstable.com/plans-quiz
- **Implementation**: `~/web/app/spaces/whitelabel/modules/whitelabel-web/packages/components/plans-quiz/`
- **Page**: `~/web/app/pages/whitelabel/plans-quiz/index.tsx`
- **Router**: `PlansQuizRouter.tsx`
- **Steps**: `plans-quiz-steps/` directory with individual step components

## Threshold: STRICT

This prototype **exactly matches production implementation**:
- Same 10-step flow order
- Same question text and labels
- Same input types and validation
- Same component patterns
- Same visual hierarchy
- Same footer structure

No exploration or experimentation — this is a pixel-perfect production replica suitable for developer handoff or UX analysis.

## Future Enhancement (Not Implemented)

The user requested this prototype as a baseline to later add a **wellness boosts upsell step** between Step 10 (Feeding Plan Type) and the final Calculating screen. That enhancement is not included in this version — this is the exact production flow only.

## Created

- **Date**: 2026-04-23
- **Brand**: The Pets Table
- **Platform**: Web
- **Threshold**: Strict
- **Source Type**: Production web repo implementation
