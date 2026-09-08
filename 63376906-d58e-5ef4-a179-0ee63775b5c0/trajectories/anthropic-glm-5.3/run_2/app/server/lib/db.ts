import pg from 'pg';

// Every timestamp and date crosses the wire as the exact string the database holds.
pg.types.setTypeParser(1082, (v) => v);
pg.types.setTypeParser(1114, (v) => v);
pg.types.setTypeParser(1184, (v) => v);

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
  idleTimeoutMillis: 30000,
});

export type Client = pg.PoolClient;

export async function query<T = any>(sql: string, params?: any[]): Promise<T[]> {
  const res = await pool.query(sql, params);
  return res.rows as T[];
}

export async function withTransaction<T>(fn: (c: Client) => Promise<T>): Promise<T> {
  const c = await pool.connect();
  try {
    await c.query('BEGIN');
    const out = await fn(c);
    await c.query('COMMIT');
    return out;
  } catch (e) {
    await c.query('ROLLBACK').catch(() => {});
    c.release();
    throw e;
  } finally {
    try { c.release(); } catch { /* already released */ }
  }
}

export function serializeTransaction<T>(fn: (c: Client) => Promise<T>): Promise<T> {
  return withTransaction(async (c) => {
    await c.query(`SET TRANSACTION ISOLATION LEVEL SERIALIZABLE`);
    return fn(c);
  });
}

export default pool;
