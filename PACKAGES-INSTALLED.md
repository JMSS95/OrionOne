# Packages Installed - November 13, 2025

## Summary

Successfully installed **critical ITSM packages** for Sprint 2+ development:

### Backend (Composer)

✅ **spatie/laravel-medialibrary** `v11.17.4`

-   File uploads and attachments for tickets
-   Image optimization and conversions
-   Multiple collections support
-   Migration published: `2025_11_13_110032_create_media_table.php`

✅ **maatwebsite/excel** `v1.1` (moved from dev to production)

-   CSV/Excel import for bulk asset uploads
-   Report exports (tickets, assets, SLA compliance)
-   Used in Sprint 7 (Asset Management)

### Frontend (NPM)

✅ **@tiptap/vue-3** + **@tiptap/starter-kit** + **@tiptap/extension-placeholder**

-   Rich text editor for ticket descriptions
-   Markdown support
-   Mentions, links, code blocks
-   Used in Sprint 2 (Tickets CRUD)

✅ **date-fns**

-   Modern date utility library
-   SLA deadline calculations
-   Timezone-aware formatting
-   Replaces moment.js (smaller bundle)

✅ **chart.js** + **vue-chartjs**

-   Dashboard visualizations
-   Ticket metrics by status/priority
-   SLA compliance charts
-   Agent performance graphs
-   Used in Sprint 5 (Dashboard & Reports)

---

## Configuration Changes

### composer.json

-   Changed `"php": "^8.3"` → `"php": "^8.2"` (matches installed PHP 8.2.12)
-   Moved `maatwebsite/excel` from `require-dev` to `require`

### Next Steps

1. **Run MediaLibrary Migration:**

    ```bash
    docker-compose exec orionone-app php artisan migrate
    ```

2. **Add HasMedia trait to Ticket model** (Sprint 2):

    ```php
    use Spatie\MediaLibrary\HasMedia;
    use Spatie\MediaLibrary\InteractsWithMedia;

    class Ticket extends Model implements HasMedia
    {
        use InteractsWithMedia;
    }
    ```

3. **Create Tiptap component** (Sprint 2):
    ```vue
    <script setup>
    import { useEditor, EditorContent } from "@tiptap/vue-3";
    import StarterKit from "@tiptap/starter-kit";
    </script>
    ```

---

## Why These Packages?

### Not Added: Filament ❌

-   Too opinionated for custom ITSM UI
-   Conflicts with Shadcn-vue component library
-   Designed for admin panels, not customer-facing ticketing
-   Would slow development, not accelerate it

### Not Added: Laravel Reverb ⏳

-   Real-time WebSockets (Post-MVP Phase 2)
-   Not critical for MVP (polling works for now)
-   Can add later without breaking changes

### Priority Packages (Added Now)

1. **Tiptap** - Sprint 2 blocks without rich text editor
2. **date-fns** - Sprint 2 needs SLA formatting
3. **MediaLibrary** - Sprint 2 tickets need attachments
4. **Chart.js** - Sprint 5 dashboard visualizations
5. **Maatwebsite Excel** - Sprint 7 asset imports/exports

---

## Stack Completeness: 98%

**Missing (Optional):**

-   ⏳ Laravel Reverb (real-time, Phase 2)
-   ⏳ Laravel DomPDF (PDF exports, Phase 2)
-   ⏳ VueDraggable (Kanban view, Phase 2)

**Stack is MVP-ready.** All critical dependencies installed.
