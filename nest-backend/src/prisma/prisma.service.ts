import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService
    extends PrismaClient
    implements OnModuleInit, OnModuleDestroy
{
    constructor() {
        super({
            log:
                process.env.NODE_ENV === 'development'
                    ? ['query', 'error', 'warn']
                    : ['error'],
        });
    }

    async onModuleInit() {
        await this.$connect();
        console.log('🔌 Prisma connected to database');
    }

    async onModuleDestroy() {
        await this.$disconnect();
        console.log('🔌 Prisma disconnected from database');
    }

    /**
     * Clean database (useful for testing)
     */
    async cleanDatabase() {
        if (process.env.NODE_ENV === 'production') {
            throw new Error('Cannot clean database in production');
        }

        const models = Reflect.ownKeys(this).filter(
            (key) => key[0] !== '_' && typeof key === 'string',
        );

        return Promise.all(
            models.map((modelKey) => (this as any)[modelKey].deleteMany()),
        );
    }
}
