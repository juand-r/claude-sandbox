/*
 * loss.c - Loss functions
 *
 * Cross-entropy loss with numerically stable softmax.
 */

#include "qat_cpu.h"

/*
 * Cross-entropy loss.
 *
 * logits: [batch x vocab_size] raw pre-softmax scores
 * targets: [batch] integer class labels (0 to vocab_size-1)
 * grad_logits: [batch x vocab_size] output gradient = softmax(logits) - one_hot(target)
 *
 * Returns mean loss over batch.
 *
 * For numerical stability, we compute:
 *   loss_i = -logits[i][target] + log(sum_j exp(logits[i][j]))
 * with the log-sum-exp trick.
 */
float cross_entropy_loss(const float *logits, const int *targets,
                         int batch, int vocab_size,
                         float *grad_logits) {
    float total_loss = 0.0f;

    for (int i = 0; i < batch; i++) {
        const float *row = &logits[i * vocab_size];
        float *grad_row = &grad_logits[i * vocab_size];

        /* Find max for numerical stability */
        float max_val = row[0];
        for (int j = 1; j < vocab_size; j++) {
            if (row[j] > max_val) max_val = row[j];
        }

        /* Compute softmax and loss */
        float sum_exp = 0.0f;
        for (int j = 0; j < vocab_size; j++) {
            float e = expf(row[j] - max_val);
            grad_row[j] = e;
            sum_exp += e;
        }

        /* Normalize to get softmax probs */
        float inv_sum = 1.0f / sum_exp;
        for (int j = 0; j < vocab_size; j++) {
            grad_row[j] *= inv_sum;
        }

        /* Loss: -log(softmax[target]) */
        float prob_target = grad_row[targets[i]];
        total_loss += -logf(fmaxf(prob_target, 1e-10f));

        /* Gradient: softmax - one_hot */
        grad_row[targets[i]] -= 1.0f;

        /* Scale gradient by 1/batch (mean loss) */
        float inv_batch = 1.0f / (float)batch;
        for (int j = 0; j < vocab_size; j++) {
            grad_row[j] *= inv_batch;
        }
    }

    return total_loss / (float)batch;
}
