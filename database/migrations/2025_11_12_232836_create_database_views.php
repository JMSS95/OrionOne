<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
 public function up(): void
 {
 // VIEW 1: Dashboard de tickets
 DB::statement("
 CREATE OR REPLACE VIEW v_ticket_dashboard AS
 SELECT
 t.id,
 t.ticket_number,
 t.title,
 t.status,
 t.priority,
 t.created_at,
 t.resolution_deadline,
 u_req.name AS requester_name,
 u_req.email AS requester_email,
 u_ag.name AS assigned_agent_name,
 tm.name AS team_name,
 CASE
 WHEN t.resolution_deadline < NOW()
 AND t.status IN ('open', 'in_progress')
 AND t.resolved_at IS NULL
 THEN true
 ELSE false
 END AS is_overdue,
 (SELECT COUNT(*) FROM comments WHERE ticket_id = t.id AND deleted_at IS NULL) AS comment_count
 FROM tickets t
 LEFT JOIN users u_req ON t.requester_id = u_req.id
 LEFT JOIN users u_ag ON t.assigned_to = u_ag.id
 LEFT JOIN teams tm ON t.team_id = tm.id
 WHERE t.deleted_at IS NULL
 ");

 // VIEW 2: SLA Compliance
 DB::statement("
 CREATE OR REPLACE VIEW v_sla_compliance AS
 SELECT
 t.id,
 t.ticket_number,
 t.priority,
 CASE
 WHEN t.first_response_at <= t.first_response_deadline THEN 'MET'
 WHEN t.first_response_at > t.first_response_deadline THEN 'BREACHED'
 WHEN t.first_response_at IS NULL AND NOW() > t.first_response_deadline THEN 'BREACHED'
 ELSE 'PENDING'
 END AS first_response_sla_status,
 CASE
 WHEN t.resolved_at <= t.resolution_deadline THEN 'MET'
 WHEN t.resolved_at > t.resolution_deadline THEN 'BREACHED'
 WHEN t.resolved_at IS NULL AND NOW() > t.resolution_deadline THEN 'BREACHED'
 ELSE 'PENDING'
 END AS resolution_sla_status
 FROM tickets t
 WHERE t.deleted_at IS NULL
 ");

 // VIEW 3: Agent Performance
 DB::statement("
 CREATE OR REPLACE VIEW v_agent_performance AS
 SELECT
 u.id AS agent_id,
 u.name AS agent_name,
 COUNT(DISTINCT t.id) AS total_tickets,
 COUNT(DISTINCT CASE WHEN t.status = 'resolved' THEN t.id END) AS resolved_tickets,
 ROUND(AVG(EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600), 2) AS avg_resolution_hours
 FROM users u
 LEFT JOIN tickets t ON u.id = t.assigned_to
 WHERE u.deleted_at IS NULL
 GROUP BY u.id, u.name
 ");
 }

 public function down(): void
 {
 DB::statement('DROP VIEW IF EXISTS v_agent_performance');
 DB::statement('DROP VIEW IF EXISTS v_sla_compliance');
 DB::statement('DROP VIEW IF EXISTS v_ticket_dashboard');
 }
};
