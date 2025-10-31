# PocketShop

| Project Members | Profile |
|-----------------|------------------|
| Shae Tran | https://github.com/shaepy |
| Bronte De Agrela | https://github.com/Bronteda |

Timeframe: 13 days

## Overview
**PocketShop is a full-stack e-commerce web application that empowers creators and small business owners to launch and manage their own online shops:**
- Create and customize shop profiles
- Upload and showcase product listings with images and details
- Manage orders and track customer purchases
- Simulate transactions through a mock payment system
- Browse shops and discover products from other vendors

Built with the Django REST Framework, PostgreSQL, and React, PocketShop features JWT authentication for secure vendor and buyer access, ensuring a smooth experience for both sides of the marketplace.

### Screenshots
<img width="480" alt="shop-page" src="https://github.com/user-attachments/assets/07f3d396-34f1-40f6-be76-d1a149721bb3" />
<img width="480" alt="product-page" src="https://github.com/user-attachments/assets/417e8e60-bca3-4d28-963c-889ca682008e" />
<img width="480" alt="manage-shop" src="https://github.com/user-attachments/assets/907d76dc-709e-4c11-a589-5e524a2f4cc4" />
<img width="480" alt="manage-orders" src="https://github.com/user-attachments/assets/b3999f59-b044-4877-ac4d-4393caa4ad7a" />
<img width="480" alt="cart" src="https://github.com/user-attachments/assets/11b3e4bb-43ae-4c54-be97-fbd3c87c9a87" />
<img width="480" alt="product-edit" src="https://github.com/user-attachments/assets/f0c1c01e-eaf2-42a0-ad43-6d75c6dc9bc8" />

---

## Technology Stack
- **Back-end**: Django, PostgreSQL, Python
- **Front-end**: React, CSS, Bulma, JavaScript
- **Tools/Storage**: Notion, Figma, Postman, Cloudinary

---

## Features

- **Shop Creation & Customization** ∙ Build your own shop with unique branding, descriptions, and cover images.
- **Product Management** ∙ Add, edit, and remove product listings with names, images, pricing, and inventory details.
- **Image Uploads** ∙ Upload and manage product photos to showcase items visually through Cloudinary integration.
- **Order Tracking** ∙ Track customer orders and fulfillment status directly from your shop dashboard.
- **Mock Payments** ∙ Simulate purchase transactions with a built-in mock payment system for testing order flow.
- **Vendor & Buyer Roles** ∙ Secure JWT authentication provides distinct access for shop owners and customers.
- **Shop Discovery** ∙ Browse other shops and explore products created by different vendors on the platform.

---

## Planning Phase

Our project management was done through Notion, utilizing a Kanban board for development. MVP stories were turned into tasks on the board, with any bugs or additional tickets being added to the backlog during the development phase.
- [Link to Full Project Plan ](https://www.notion.so/Unit-4-PocketShop-Django-React-2887ed1fdd5880fba01dc0835c2de26e?source=copy_link)
- [Kanban Board](https://www.notion.so/28d7ed1fdd58817d9bd7e89a190d9ad3?v=28d7ed1fdd5881df8b9b000c646107d9&source=copy_link)

This was our main hub for collaborative work and documentation to align on endpoints, routes, database structure, MVP stories, user flows, wireframes, and research on external APIs.

### Wireframes

<img width="400" alt="image4" src="https://github.com/user-attachments/assets/ed41d57a-167f-42e7-b9bd-ab266b1fc39a" />
<img width="400" alt="image3" src="https://github.com/user-attachments/assets/59372fe0-50d4-4b8b-8354-6f0e896737d9" />
<img width="400" alt="image2" src="https://github.com/user-attachments/assets/14fb203e-2291-46a4-97a9-1deeef6f8e60" />

---

## Data Models & Entity Relationship Diagram (ERD)
<img width="800" alt="pocketshop_erd" src="https://github.com/user-attachments/assets/f6d1d3c8-a83b-4528-99ba-45d430248f20" />

Since this was my first time working with Django and PostgreSQL, I focused on building a strong understanding of how each model interacts with others. Our ERD went through several iterations as we refined relationships between tables, learning the nuances of OneToOneField, ForeignKey, and ManyToManyField.

Designing the data structure was one of the more challenging parts of development, as incorrect relationship types occasionally caused conflicts. Through testing, debugging, and iterative refinement, we gained a deeper understanding of Django’s ORM and relational database design.

---
## Git Collaboration & Workflow

PocketShop was developed collaboratively, with both myself and my partner working across different time zones. One developer’s morning overlapped with the other’s evening, so we used that window like a daily standup to discuss progress, blockers, and new findings.

We followed a branch-based workflow, creating separate branches from `main` for each feature or model. For example, one of us might develop the `Product` endpoints while the other built out `Cart` functionality. After completing a task, we committed and pushed changes to our respective branches, opening a pull request for review before merging. This approach ensured smooth coordination, timely conflict resolution, and uninterrupted development even while working asynchronously.

---

## Challenges
1. **Image Uploads & Cloudinary** - Integrating Cloudinary for image uploads was a key challenge, especially in managing how data was sent between React and Django REST. We had to ensure the correct values, such as `secure_url`, were passed back to the backend, which became tricky during PUT requests when editing products or shops. Through testing and debugging, we refined how files were uploaded, stored, and updated to maintain secure and reliable image handling across the app.
2. **ERD & Data Models** - Built with Django and PostgreSQL, another one of our early challenges was learning how to structure models and define relationships correctly. Understanding Django’s ORM and how ForeignKey, OneToOneField, and ManyToManyField worked in practice required multiple iterations of our ERD. Refining these relationships helped us strengthen our database design and prevent conflicts during development.

## Wins and Key Learnings

### Mock Payments Integration

A major win for this project was successfully implementing a mock payment system. Although we didn’t have time to integrate third-party services like Stripe or PayPal sandbox, building our own mock service helped us understand the payment flow and best practices that would translate seamlessly to real APIs.

I created a serializer to validate incoming data from React, used a dataclass to structure an AuthResult, and implemented an authorize() method to handle mock authorization and return a valid response string. For this demo, the system only verifies the expiration date of the mock payment due to limited testing time. Payments were only created after successful authorization, and each payment was linked to an order record to complete the transaction workflow.

```
@dataclass
class AuthResult:
    ok: bool
    auth_id: str | None = None


class MockPaymentService:
    def authorize(self, *, exp_month: int, exp_year: int) -> AuthResult:
        # Serializer already guarantees card is not expired
        return AuthResult(ok=True, auth_id=f"mock_auth_{get_random_string(8)}")
```

### Image Uploads using Cloudinary

Another win was designing a scalable way to handle product images. We created a `ProductImage` model linked to products via `ForeignKey`, allowing multiple images per item. To manage uploads and edits, we built two serializers: one for validating incoming Cloudinary data and another for full model serialization. This approach ensured flexibility between new and existing images and made our upload system more reliable and maintainable.

```
# Added to Product model

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images")
    public_id = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

```
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class IncomingProductImageSerializer(serializers.Serializer):
    public_id = serializers.CharField()
    # Accept either secure_url (new uploads from Cloudinary) or url (existing images being kept)
    secure_url = serializers.URLField(required=False)
    url = serializers.URLField(required=False)

    def validate(self, data):
        # Ensure at least one URL field is provided
        if not data.get('secure_url') and not data.get('url'):
            raise serializers.ValidationError(
                "Either 'secure_url' or 'url' must be provided")
        # Normalize: if both provided, prefer secure_url; otherwise use whichever is present
        if not data.get('url'):
            data['url'] = data.get('secure_url')
        return data
```

---

## Future Improvements 
1. **Stripe Payment Integration** ∙ Implement real payment gateways such as Stripe or PayPal Sandbox to replace the mock payment service.
2. **Product Reviews** ∙ Add a Review model that allows buyers to leave ratings and feedback after completing a purchase.
3. **Search & Filtering** ∙ Introduce product filtering and search functionality to improve product discovery and user experience.
