# How to Add Images and Logos to Posts

## Company Logos

Each post can feature up to 3 companies with cute little logos next to their names.

### Steps:

1. **Add your company logo to the logos folder:**
   ```
   public/images/logos/company-name.svg
   ```

2. **Reference it in your post's frontmatter:**
   ```yaml
   ---
   title: "Your Post Title"
   companies:
     - name: "Stripe"
       logo: "/images/logos/stripe.svg"
     - name: "GitHub"
       logo: "/images/logos/github.svg"
   verdict: "good"
   summary: "Brief summary"
   date: 2025-10-23
   ---
   ```

### Logo Guidelines
- **Size**: 28x28px (square SVG recommended)
- **Format**: SVG preferred, PNG also works
- **Style**: Simple, recognizable, high contrast
- **Colors**: Use brand colors or monochrome
- **Optional**: Logos are optional - you can omit the `logo` field

### Example with 1-3 Companies

**Single company:**
```yaml
companies:
  - name: "Stripe"
    logo: "/images/logos/stripe.svg"
```

**Multiple companies:**
```yaml
companies:
  - name: "Stripe"
    logo: "/images/logos/stripe.svg"
  - name: "Shopify"
    logo: "/images/logos/shopify.svg"
  - name: "Square"
    logo: "/images/logos/square.svg"
```

**Company without logo:**
```yaml
companies:
  - name: "Acme Corp"
```

---

# How to Add Images to Posts

## Hero Images (Featured Image)

Hero images appear at the top of each post page and in the gallery cards.

### Steps:

1. **Add your image to the public folder:**
   ```
   public/images/your-image-name.jpg
   ```

2. **Reference it in your post's frontmatter:**
   ```yaml
   ---
   title: "Your Post Title"
   company: "Company Name"
   verdict: "good"
   summary: "Brief summary"
   date: 2025-10-23
   heroImage: "/images/your-image-name.jpg"  # ← Add this line
   tags: ["api", "schema"]
   ---
   ```

## Images Within Post Content

You can also add images within your markdown content:

### Option 1: Using Public Folder (Recommended)

1. **Add image to public folder:**
   ```
   public/images/inline-screenshot.png
   ```

2. **Reference in markdown:**
   ```markdown
   ![Description of image](/images/inline-screenshot.png)
   ```

### Option 2: External Images

You can also link to external images:

```markdown
![Alt text](https://example.com/image.jpg)
```

## Image Best Practices

### File Organization
```
public/
├── images/
│   ├── stripe-hero.jpg           # Hero images
│   ├── github-api-hero.png
│   ├── stripe-screenshot-1.png   # Inline images
│   └── stripe-screenshot-2.png
```

### Naming Convention
- Use lowercase, kebab-case: `company-name-description.jpg`
- Be descriptive: `stripe-checkout-flow.jpg` not `image1.jpg`

### Image Sizes
- **Hero images**: 1200x675px (16:9 ratio) recommended
- **Inline images**: Max 1000px width
- Keep file sizes under 500KB when possible

### Supported Formats
- `.jpg` / `.jpeg` - Best for photos
- `.png` - Best for screenshots with text
- `.webp` - Modern format, smaller file sizes
- `.svg` - Vector graphics, icons

## Example Post with Images

```markdown
---
title: "Stripe's Excellent Payment API"
company: "Stripe"
verdict: "good"
summary: "Clear documentation and structured responses"
date: 2025-10-23
heroImage: "/images/stripe-api-hero.jpg"
tags: ["api", "payments"]
---

## Overview

Stripe provides excellent documentation for developers.

![Stripe Dashboard](/images/stripe-dashboard.png)

The API responses are well-structured:

![API Response Example](/images/stripe-response-example.png)
```

## Tips

1. **Optimize images** before uploading using tools like:
   - [TinyPNG](https://tinypng.com/) for compression
   - [Squoosh](https://squoosh.app/) for format conversion

2. **Alt text matters** for accessibility:
   ```markdown
   ![Stripe's checkout flow showing clear pricing](/images/stripe-checkout.jpg)
   ```

3. **Use relative paths** starting with `/` for public folder images:
   - ✅ `/images/photo.jpg`
   - ❌ `./images/photo.jpg`
   - ❌ `images/photo.jpg`
