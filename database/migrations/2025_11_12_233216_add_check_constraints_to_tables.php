<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
 public function up(): void
 {
 // Tickets: Status enum validation
 DB::statement("
 ALTER TABLE tickets ADD CONSTRAINT chk_tickets_status
 CHECK (status IN ('open', 'in_progress', 'on_hold', 'resolved', 'closed'))
 ");

 // Tickets: Priority enum validation
 DB::statement("
 ALTER TABLE tickets ADD CONSTRAINT chk_tickets_priority
 CHECK (priority IN ('low', 'medium', 'high', 'urgent'))
 ");

 // Tickets: Date logic
 DB::statement("
 ALTER TABLE tickets ADD CONSTRAINT chk_tickets_resolved_date
 CHECK (resolved_at IS NULL OR resolved_at >= created_at)
 ");

 // Users: Email format
 DB::statement("
 ALTER TABLE users ADD CONSTRAINT chk_users_email_format
 CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
 ");
 }

 public function down(): void
 {
 DB::statement('ALTER TABLE users DROP CONSTRAINT IF EXISTS chk_users_email_format');
 DB::statement('ALTER TABLE tickets DROP CONSTRAINT IF EXISTS chk_tickets_resolved_date');
 DB::statement('ALTER TABLE tickets DROP CONSTRAINT IF EXISTS chk_tickets_priority');
 DB::statement('ALTER TABLE tickets DROP CONSTRAINT IF EXISTS chk_tickets_status');
 }
};
