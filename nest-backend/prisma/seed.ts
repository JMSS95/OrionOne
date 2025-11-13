import { PrismaClient, Role } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
    console.log('🌱 Starting seed...');

    // Clean existing data (development only)
    if (process.env.NODE_ENV !== 'production') {
        console.log('🗑️  Cleaning database...');
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

    // 1. Create Permissions (32 total)
    console.log('📝 Creating permissions...');
    const permissionGroups = [
        // Tickets (8)
        ['tickets.create', 'tickets.view', 'tickets.update', 'tickets.delete', 
         'tickets.assign', 'tickets.close', 'tickets.reopen', 'tickets.export'],
        // Users (4)
        ['users.create', 'users.view', 'users.update', 'users.delete'],
        // Categories (4)
        ['categories.create', 'categories.view', 'categories.update', 'categories.delete'],
        // Teams (4)
        ['teams.create', 'teams.view', 'teams.update', 'teams.delete'],
        // Articles (4)
        ['articles.create', 'articles.view', 'articles.update', 'articles.delete'],
        // Assets (4)
        ['assets.create', 'assets.view', 'assets.update', 'assets.delete'],
        // Reports (4)
        ['reports.view', 'reports.export', 'reports.dashboard', 'reports.analytics'],
    ];

    const permissions = await Promise.all(
        permissionGroups.flat().map((name) =>
            prisma.permission.create({
                data: {
                    name,
                    guardName: 'web', // Default guard name for web routes
                },
            }),
        ),
    );

    console.log(`✅ Created ${permissions.length} permissions`);

    // 2. Create RoleHasPermissions mapping
    console.log('🔐 Mapping permissions to roles...');

    // ADMIN: all permissions
    const adminPerms = await prisma.roleHasPermission.createMany({
        data: permissions.map((perm) => ({
            roleName: Role.ADMIN,
            permissionId: perm.id,
        })),
    });

    // AGENT: tickets, categories, teams, articles (no users, assets, reports)
    const agentPermissionNames = [
        ...permissionGroups[0], // tickets.*
        'categories.view',
        'teams.view',
        ...permissionGroups[4], // articles.*
    ];
    const agentPerms = await prisma.roleHasPermission.createMany({
        data: permissions
            .filter((p) => agentPermissionNames.includes(p.name))
            .map((perm) => ({
                roleName: Role.AGENT,
                permissionId: perm.id,
            })),
    });

    // USER: limited to own tickets + view articles
    const userPermissionNames = [
        'tickets.create',
        'tickets.view',
        'articles.view',
    ];
    const userPerms = await prisma.roleHasPermission.createMany({
        data: permissions
            .filter((p) => userPermissionNames.includes(p.name))
            .map((perm) => ({
                roleName: Role.USER,
                permissionId: perm.id,
            })),
    });

    console.log(
        `✅ Mapped permissions: ADMIN (${adminPerms.count}), AGENT (${agentPerms.count}), USER (${userPerms.count})`,
    );

    // 3. Create Test Users
    console.log('👥 Creating users...');
    const hashedPassword = await bcrypt.hash('password123', 10);

    const adminUser = await prisma.user.create({
        data: {
            name: 'Admin User',
            email: 'admin@orionone.test',
            password: hashedPassword,
            role: Role.ADMIN,
            emailVerifiedAt: new Date(),
        },
    });

    const agentUser = await prisma.user.create({
        data: {
            name: 'Agent User',
            email: 'agent@orionone.test',
            password: hashedPassword,
            role: Role.AGENT,
            emailVerifiedAt: new Date(),
        },
    });

    const normalUser = await prisma.user.create({
        data: {
            name: 'Normal User',
            email: 'user@orionone.test',
            password: hashedPassword,
            role: Role.USER,
            emailVerifiedAt: new Date(),
        },
    });

    console.log('✅ Created 3 users (admin, agent, user)');

    // 4. Create Categories
    console.log('📁 Creating categories...');
    const categories = await Promise.all([
        prisma.category.create({
            data: {
                name: 'Hardware',
                slug: 'hardware',
                description: 'Hardware issues (laptops, desktops, peripherals)',
            },
        }),
        prisma.category.create({
            data: {
                name: 'Software',
                slug: 'software',
                description: 'Software problems (applications, licenses)',
            },
        }),
        prisma.category.create({
            data: {
                name: 'Network',
                slug: 'network',
                description: 'Network connectivity and VPN issues',
            },
        }),
        prisma.category.create({
            data: {
                name: 'Access',
                slug: 'access',
                description: 'Access requests and permissions',
            },
        }),
        prisma.category.create({
            data: {
                name: 'Other',
                slug: 'other',
                description: 'Miscellaneous issues',
            },
        }),
    ]);

    console.log(`✅ Created ${categories.length} categories`);

    // 5. Create Sample Tickets
    console.log('🎫 Creating sample tickets...');
    const tickets = await Promise.all([
        // Ticket 1: OPEN - Hardware
        prisma.ticket.create({
            data: {
                ticketNumber: 'TKT-2024-0001',
                title: 'Laptop screen flickering',
                description:
                    'My laptop screen has been flickering intermittently for the past 2 days. It happens mostly when I open heavy applications like Chrome with multiple tabs.',
                status: 'OPEN',
                priority: 'HIGH',
                requesterId: normalUser.id,
                categoryId: categories[0].id, // Hardware
            },
        }),
        // Ticket 2: IN_PROGRESS - Software
        prisma.ticket.create({
            data: {
                ticketNumber: 'TKT-2024-0002',
                title: 'Microsoft Office activation failed',
                description:
                    'Cannot activate Microsoft Office 365. Getting error code 0x80070426.',
                status: 'IN_PROGRESS',
                priority: 'MEDIUM',
                requesterId: normalUser.id,
                assignedTo: agentUser.id,
                categoryId: categories[1].id, // Software
            },
        }),
        // Ticket 3: ON_HOLD - Network
        prisma.ticket.create({
            data: {
                ticketNumber: 'TKT-2024-0003',
                title: 'VPN connection timeout',
                description:
                    'VPN connection times out after 5 minutes. Need to reconnect frequently.',
                status: 'ON_HOLD',
                priority: 'LOW',
                requesterId: normalUser.id,
                assignedTo: agentUser.id,
                categoryId: categories[2].id, // Network
            },
        }),
        // Ticket 4: RESOLVED - Access
        prisma.ticket.create({
            data: {
                ticketNumber: 'TKT-2024-0004',
                title: 'Request access to shared drive',
                description:
                    'Need read/write access to the Marketing shared drive (\\\\server\\marketing).',
                status: 'RESOLVED',
                priority: 'MEDIUM',
                requesterId: normalUser.id,
                assignedTo: agentUser.id,
                categoryId: categories[3].id, // Access
                resolvedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
            },
        }),
        // Ticket 5: URGENT - Hardware
        prisma.ticket.create({
            data: {
                ticketNumber: 'TKT-2024-0005',
                title: 'Desktop computer not booting',
                description:
                    'Workstation in office 302 is not booting. Black screen with "No bootable device" error.',
                status: 'OPEN',
                priority: 'URGENT',
                requesterId: agentUser.id,
                categoryId: categories[0].id, // Hardware
            },
        }),
    ]);

    console.log(`✅ Created ${tickets.length} sample tickets`);

    // 6. Create Comments on Tickets
    console.log('💬 Creating comments...');
    await prisma.comment.createMany({
        data: [
            {
                content:
                    'I have checked the laptop, seems to be a graphics driver issue. Will update drivers and test.',
                ticketId: tickets[0].id,
                userId: agentUser.id,
            },
            {
                content:
                    'Drivers updated successfully. Please test and confirm if the issue persists.',
                ticketId: tickets[0].id,
                userId: agentUser.id,
            },
            {
                content:
                    'I have generated a new license key. Please use this key: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX',
                ticketId: tickets[1].id,
                userId: agentUser.id,
            },
            {
                content:
                    'Waiting for network team to investigate VPN server logs.',
                ticketId: tickets[2].id,
                userId: agentUser.id,
            },
            {
                content:
                    'Access granted. You should now be able to access the Marketing shared drive.',
                ticketId: tickets[3].id,
                userId: agentUser.id,
            },
        ],
    });

    console.log('✅ Created 5 comments on tickets');

    // 7. Create a Team
    console.log('👨‍💼 Creating teams...');
    const supportTeam = await prisma.team.create({
        data: {
            name: 'IT Support Team',
            slug: 'it-support-team',
            description: 'First-line technical support',
        },
    });

    await prisma.teamMember.createMany({
        data: [
            { teamId: supportTeam.id, userId: agentUser.id, role: 'LEAD' },
            { teamId: supportTeam.id, userId: adminUser.id, role: 'MEMBER' },
        ],
    });

    console.log('✅ Created 1 team with 2 members');

    console.log('🎉 Seed completed successfully!');
    console.log('\n📊 Summary:');
    console.log(`   - ${permissions.length} permissions`);
    console.log(
        `   - ${adminPerms.count + agentPerms.count + userPerms.count} role-permission mappings`,
    );
    console.log('   - 3 users (admin, agent, user)');
    console.log(`   - ${categories.length} categories`);
    console.log(`   - ${tickets.length} tickets`);
    console.log('   - 5 comments');
    console.log('   - 1 team with 2 members');
    console.log('\n🔑 Test credentials:');
    console.log('   - admin@orionone.test / password123 (ADMIN)');
    console.log('   - agent@orionone.test / password123 (AGENT)');
    console.log('   - user@orionone.test / password123 (USER)');
}

main()
    .catch((e) => {
        console.error('❌ Seed failed:', e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
