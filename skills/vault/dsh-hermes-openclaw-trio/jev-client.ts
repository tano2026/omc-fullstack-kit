/**
 * TypeSafe AI - JEV System One Decision Engine Client
 * Fast (~10-50ms), deterministic, non-generative probabilistic decision primitive.
 */

export interface JevConfig {
  apiKey?: string;
  baseUrl?: string;
  model?: string;
  safetyThreshold?: number; // 0 - 100 risk score
}

export interface JevDecision<T = any> {
  value: T;
  confidence: number;
  latencyMs: number;
  source: 'typesafe_api' | 'local_reflex_engine';
}

export class JevClient {
  private config: JevConfig;

  constructor(config?: JevConfig) {
    this.config = {
      apiKey: config?.apiKey || process.env.JEV_API_KEY || '',
      baseUrl: config?.baseUrl || process.env.JEV_BASE_URL || 'https://api.typesafe.ai/v1/systemone',
      model: config?.model || 'jev-system-one-v1',
      safetyThreshold: config?.safetyThreshold ?? 70,
    };
  }

  /**
   * Primitive 1: Choice
   * Given context and options, select the most accurate option deterministically.
   */
  public async choice<T extends string>(context: string, question: string, options: T[]): Promise<JevDecision<T>> {
    const start = Date.now();

    if (this.config.apiKey) {
      try {
        const res = await fetch(this.config.baseUrl!, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.config.apiKey}`,
          },
          body: JSON.stringify({
            model: this.config.model,
            type: 'choice',
            context,
            question,
            options,
          }),
        });

        if (res.ok) {
          const data = await res.json() as any;
          return {
            value: data.selection as T,
            confidence: data.confidence ?? 0.95,
            latencyMs: Date.now() - start,
            source: 'typesafe_api',
          };
        }
      } catch {
        // Fallback to local reflex engine
      }
    }

    // Local high-speed reflex heuristic engine
    const selected = this.localReflexChoice(context, question, options);
    return {
      value: selected,
      confidence: 0.9,
      latencyMs: Date.now() - start,
      source: 'local_reflex_engine',
    };
  }

  /**
   * Primitive 2: Score
   * Evaluates context on a numeric scale (0 - 100).
   */
  public async score(context: string, question: string): Promise<JevDecision<number>> {
    const start = Date.now();

    if (this.config.apiKey) {
      try {
        const res = await fetch(this.config.baseUrl!, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.config.apiKey}`,
          },
          body: JSON.stringify({
            model: this.config.model,
            type: 'score',
            context,
            question,
            min: 0,
            max: 100,
          }),
        });

        if (res.ok) {
          const data = await res.json() as any;
          return {
            value: Number(data.score),
            confidence: data.confidence ?? 0.95,
            latencyMs: Date.now() - start,
            source: 'typesafe_api',
          };
        }
      } catch {
        // Fallback
      }
    }

    const calculatedScore = this.localReflexScore(context, question);
    return {
      value: calculatedScore,
      confidence: 0.88,
      latencyMs: Date.now() - start,
      source: 'local_reflex_engine',
    };
  }

  /**
   * Primitive 3: Noul (Boolean Yes/No)
   * Probabilistic binary evaluation.
   */
  public async noul(context: string, question: string): Promise<JevDecision<boolean>> {
    const start = Date.now();

    if (this.config.apiKey) {
      try {
        const res = await fetch(this.config.baseUrl!, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.config.apiKey}`,
          },
          body: JSON.stringify({
            model: this.config.model,
            type: 'noul',
            context,
            question,
          }),
        });

        if (res.ok) {
          const data = await res.json() as any;
          return {
            value: Boolean(data.result),
            confidence: data.confidence ?? 0.95,
            latencyMs: Date.now() - start,
            source: 'typesafe_api',
          };
        }
      } catch {
        // Fallback
      }
    }

    const isTrue = this.localReflexNoul(context, question);
    return {
      value: isTrue,
      confidence: 0.92,
      latencyMs: Date.now() - start,
      source: 'local_reflex_engine',
    };
  }

  // --- Local Reflex Heuristics (Zero-Latency Fallback) ---

  private localReflexChoice<T extends string>(context: string, question: string, options: T[]): T {
    const lowerCtx = context.toLowerCase();
    const lowerQ = question.toLowerCase();

    // Intent routing heuristics
    if (options.includes('direct_reply' as T) && (lowerCtx.includes('chào') || lowerCtx.includes('hello') || lowerCtx.includes('ping'))) {
      return 'direct_reply' as T;
    }
    if (options.includes('dsh' as T) && (lowerCtx.includes('goal') || lowerCtx.includes('kế hoạch') || lowerCtx.includes('feature') || lowerCtx.includes('refactor'))) {
      return 'dsh' as T;
    }
    if (options.includes('hermes' as T) && (lowerCtx.includes('thuật toán') || lowerCtx.includes('debug') || lowerCtx.includes('tối ưu') || lowerCtx.includes('review'))) {
      return 'hermes' as T;
    }
    if (options.includes('openclaw' as T) && (lowerCtx.includes('chạy') || lowerCtx.includes('deploy') || lowerCtx.includes('git') || lowerCtx.includes('terminal'))) {
      return 'openclaw' as T;
    }

    return options[0];
  }

  private localReflexScore(context: string, question: string): number {
    const lower = context.toLowerCase();
    let score = 10;

    // Destructive keywords check
    const criticalPatterns = ['rm -rf', 'drop table', 'delete from', 'truncate', 'format c:', 'mkfs', '> /dev/sda', 'chmod 777 -r'];
    const highRiskPatterns = ['npm run build', 'kill -9', 'pm2 restart', 'git push --force', 'git reset --hard', 'scp -r'];

    if (criticalPatterns.some(p => lower.includes(p))) {
      score = 95;
    } else if (highRiskPatterns.some(p => lower.includes(p))) {
      score = 75;
    } else if (lower.includes('deploy') || lower.includes('update') || lower.includes('sudo')) {
      score = 50;
    }

    return score;
  }

  private localReflexNoul(context: string, question: string): boolean {
    const lower = context.toLowerCase();
    const lowerQ = question.toLowerCase();

    if (lowerQ.includes('destructive') || lowerQ.includes('danger') || lowerQ.includes('risk')) {
      return this.localReflexScore(context, question) >= (this.config.safetyThreshold ?? 70);
    }

    if (lowerQ.includes('pass') || lowerQ.includes('success')) {
      return !lower.includes('fail') && !lower.includes('error') && !lower.includes('exception');
    }

    return false;
  }
}
