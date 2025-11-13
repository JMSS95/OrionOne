<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
 public function up(): void
 {
 // FUNCTION: Generate ticket_number
 DB::statement("
 CREATE OR REPLACE FUNCTION generate_ticket_number()
 RETURNS TRIGGER AS $$
 DECLARE
 date_prefix TEXT;
 seq_num INTEGER;
 BEGIN
 IF NEW.ticket_number IS NOT NULL THEN
 RETURN NEW;
 END IF;

 date_prefix := TO_CHAR(NOW(), 'YYYYMMDD');

 SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_number FROM 13) AS INTEGER)), 0) + 1
 INTO seq_num
 FROM tickets
 WHERE ticket_number LIKE 'TKT-' || date_prefix || '-%';

 NEW.ticket_number := 'TKT-' || date_prefix || '-' || LPAD(seq_num::TEXT, 4, '0');
 RETURN NEW;
 END;
 $$ LANGUAGE plpgsql;
 ");

 DB::statement("
 CREATE TRIGGER trg_generate_ticket_number
 BEFORE INSERT ON tickets
 FOR EACH ROW
 WHEN (NEW.ticket_number IS NULL)
 EXECUTE FUNCTION generate_ticket_number()
 ");

 // FUNCTION: Set SLA deadlines
 DB::statement("
 CREATE OR REPLACE FUNCTION set_sla_deadlines()
 RETURNS TRIGGER AS $$
 BEGIN
 NEW.first_response_deadline := NEW.created_at +
 CASE NEW.priority
 WHEN 'urgent' THEN INTERVAL '2 hours'
 WHEN 'high' THEN INTERVAL '4 hours'
 WHEN 'medium' THEN INTERVAL '8 hours'
 WHEN 'low' THEN INTERVAL '24 hours'
 END;

 NEW.resolution_deadline := NEW.created_at +
 CASE NEW.priority
 WHEN 'urgent' THEN INTERVAL '8 hours'
 WHEN 'high' THEN INTERVAL '2 days'
 WHEN 'medium' THEN INTERVAL '5 days'
 WHEN 'low' THEN INTERVAL '10 days'
 END;

 RETURN NEW;
 END;
 $$ LANGUAGE plpgsql;
 ");

 DB::statement("
 CREATE TRIGGER trg_set_sla_deadlines
 BEFORE INSERT ON tickets
 FOR EACH ROW
 EXECUTE FUNCTION set_sla_deadlines()
 ");
 }

 public function down(): void
 {
 DB::statement('DROP TRIGGER IF EXISTS trg_set_sla_deadlines ON tickets');
 DB::statement('DROP FUNCTION IF EXISTS set_sla_deadlines');
 DB::statement('DROP TRIGGER IF EXISTS trg_generate_ticket_number ON tickets');
 DB::statement('DROP FUNCTION IF EXISTS generate_ticket_number');
 }
};
