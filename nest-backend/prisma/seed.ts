import { PrismaClient, Role } from '@prisma/client';
import { hash } from 'bcrypt';

const prisma = new PrismaClient();
const SALT_ROUNDS = 10;

const PERMISSIONS = {
    TICKETS: [
        'tickets.create',
        'tickets.view',
        'tickets.update',
        'tickets.delete',
        'tickets.assign',
        'tickets.close',
        'tickets.reopen',
        'tickets.export',
    ],
    USERS: ['users.create', 'users.view', 'users.update', 'users.delete'],
    CATEGORIES: [
        'categories.create',
        'categories.view',
        'categories.update',
        'categories.delete',
    ],
    TEAMS: ['teams.create', 'teams.view', 'teams.update', 'teams.delete'],
    ARTICLES: [
        'articles.create',
        'articles.view',
        'articles.update',
        'articles.delete',
    ],
    ASSETS: ['assets.create', 'assets.view', 'assets.update', 'assets.delete'],
    REPORTS: [
        'reports.view',
        'reports.export',
        'reports.dashboard',
        'reports.analytics',
    ],
} as const;

const ROLE_PERMISSIONS = {
    [Role.ADMIN]: Object.values(PERMISSIONS).flat(),
    [Role.AGENT]: [
        ...PERMISSIONS.TICKETS,
        'categories.view',
        'teams.view',
        ...PERMISSIONS.ARTICLES,
    ],
    [Role.USER]: ['tickets.create', 'tickets.view', 'articles.view'],
} as const;

async function cleanDatabase() {
    if (process.env.NODE_ENV === 'production') return;

    await prisma.roleHasPermission.deleteMany();
    await prisma.permission.deleteMany();
    await prisma.comment.deleteMany();
    await prisma.ticket.deleteMany();
    await prisma.category.deleteMany();
    await prisma.teamMember.deleteMany();
    await prisma.team.deleteMany();
    await prisma.articleVersion.deleteMany();
    await prisma.article.deleteMany();
    await prisma.asset.deleteMany();
    await prisma.media.deleteMany();
    await prisma.activityLog.deleteMany();
    await prisma.notification.deleteMany();
    await prisma.user.deleteMany();
}

async function createPermissions() {
    const allPermissions = Object.values(PERMISSIONS).flat();
    const permissions = await Promise.all(
        allPermissions.map((name) =>
            prisma.permission.create({
                data: { name, guardName: 'api' },
            }),
        ),
    );

    return permissions;
}

async function assignRolePermissions(
    permissions: { id: string; name: string }[],
) {
    const permissionMap = new Map(permissions.map((p) => [p.name, p.id]));

    for (const [role, permNames] of Object.entries(ROLE_PERMISSIONS)) {
        const rolePermissions = permNames
            .map((name) => permissionMap.get(name))
            .filter((id): id is string => id !== undefined)
            .map((permissionId) => ({
                roleName: role as Role,
                permissionId,
            }));

        await prisma.roleHasPermission.createMany({
            data: rolePermissions,
        });
    }
}

async function createUsers() {
    const password = await hash('password123', SALT_ROUNDS);

    const users = await Promise.all([
        prisma.user.create({
            data: {
                name: 'Admin User',
                email: 'admin@orionone.test',
                password,
                role: Role.ADMIN,
                emailVerifiedAt: new Date(),
            },
        }),
        prisma.user.create({
            data: {
                name: 'Agent User',
                email: 'agent@orionone.test',
                password,
                role: Role.AGENT,
                emailVerifiedAt: new Date(),
            },
        }),
        prisma.user.create({
            data: {
                name: 'Normal User',
                email: 'user@orionone.test',
                password,
                role: Role.USER,
                emailVerifiedAt: new Date(),
            },
        }),
    ]);

    return users;
}

async function createCategories() {
    const categoryData = [
        {
            name: 'Hardware',
            slug: 'hardware',
            description: 'Hardware issues (laptops, desktops, peripherals)',
        },
        {
            name: 'Software',
            slug: 'software',
            description: 'Software problems (applications, licenses)',
        },
        {
            name: 'Network',
            slug: 'network',
            description: 'Network connectivity and VPN issues',
        },
        {
            name: 'Access',
            slug: 'access',
            description: 'Access requests and permissions',
        },
        {
            name: 'Other',
            slug: 'other',
            description: 'Miscellaneous issues',
        },
    ];

    const categories = await Promise.all(
        categoryData.map((data) => prisma.category.create({ data })),
    );

    return categories;
}

async function createTickets(
    users: { id: string }[],
    categories: { id: string }[],
) {
    const agent = users[1];
    const user = users[2];
    const [hardware, software, network, access] = categories;

    const ticketData = [
        {
            ticketNumber: 'TKT-2024-0001',
            title: 'Laptop screen flickering',
            description:
                'Laptop screen flickering intermittently for 2 days. Happens with heavy applications.',
            status: 'OPEN' as const,
            priority: 'HIGH' as const,
            requesterId: user.id,
            categoryId: hardware.id,
        },
        {
            ticketNumber: 'TKT-2024-0002',
            title: 'Office activation failed',
            description:
                'Cannot activate Microsoft Office 365. Error code 0x80070426.',
            status: 'IN_PROGRESS' as const,
            priority: 'MEDIUM' as const,
            requesterId: user.id,
            assignedTo: agent.id,
            categoryId: software.id,
        },
        {
            ticketNumber: 'TKT-2024-0003',
            title: 'VPN connection timeout',
            description:
                'VPN connection times out after 5 minutes. Frequent reconnects needed.',
            status: 'ON_HOLD' as const,
            priority: 'LOW' as const,
            requesterId: user.id,
            assignedTo: agent.id,
            categoryId: network.id,
        },
        {
            ticketNumber: 'TKT-2024-0004',
            title: 'Shared drive access request',
            description: 'Need read/write access to Marketing shared drive.',
            status: 'RESOLVED' as const,
            priority: 'MEDIUM' as const,
            requesterId: user.id,
            assignedTo: agent.id,
            categoryId: access.id,
            resolvedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
        },
        {
            ticketNumber: 'TKT-2024-0005',
            title: 'Desktop not booting',
            description:
                'Workstation in office 302 not booting. Black screen error.',
            status: 'OPEN' as const,
            priority: 'URGENT' as const,
            requesterId: agent.id,
            categoryId: hardware.id,
        },
    ];

    const tickets = await Promise.all(
        ticketData.map((data) => prisma.ticket.create({ data })),
    );

    return tickets;
}

async function createComments(
    tickets: { id: string }[],
    users: { id: string }[],
) {
    const agent = users[1];

    const commentData = [
        {
            content: 'Checking laptop. Likely graphics driver issue.',
            ticketId: tickets[0].id,
            userId: agent.id,
        },
        {
            content: 'Drivers updated. Please test.',
            ticketId: tickets[0].id,
            userId: agent.id,
        },
        {
            content: 'New license key generated: XXXXX-XXXXX-XXXXX',
            ticketId: tickets[1].id,
            userId: agent.id,
        },
        {
            content: 'Waiting for network team to check VPN logs.',
            ticketId: tickets[2].id,
            userId: agent.id,
        },
        {
            content: 'Access granted. Check Marketing shared drive.',
            ticketId: tickets[3].id,
            userId: agent.id,
        },
    ];

    await prisma.comment.createMany({ data: commentData });
}

async function createTeam(users: { id: string }[]) {
    const [admin, agent] = users;

    const team = await prisma.team.create({
        data: {
            name: 'IT Support Team',
            slug: 'it-support-team',
            description: 'First-line technical support',
        },
    });

    await prisma.teamMember.createMany({
        data: [
            { teamId: team.id, userId: agent.id, role: 'LEAD' },
            { teamId: team.id, userId: admin.id, role: 'MEMBER' },
        ],
    });

    return team;
}

async function main() {
    console.log('Starting database seed...');

    await cleanDatabase();
    console.log('Database cleaned');

    const permissions = await createPermissions();
    console.log(`Created ${permissions.length} permissions`);

    await assignRolePermissions(permissions);
    console.log('Assigned role permissions');

    const users = await createUsers();
    console.log('Created 3 users');

    const categories = await createCategories();
    console.log('Created 5 categories');

    const tickets = await createTickets(users, categories);
    console.log('Created 5 tickets');

    await createComments(tickets, users);
    console.log('Created 5 comments');

    await createTeam(users);
    console.log('Created 1 team');

    console.log('\nSeed completed successfully');
    console.log('\nTest credentials:');
    console.log('  admin@orionone.test / password123 (ADMIN)');
    console.log('  agent@orionone.test / password123 (AGENT)');
    console.log('  user@orionone.test / password123 (USER)');
}

main()
    .catch((error) => {
        console.error('Seed failed:', error);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
