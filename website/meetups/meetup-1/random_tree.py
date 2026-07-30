

# This function randomly creates a tree-like function
# Evaluated on a linspace vector

def random_tree(x,num_splits):

    # Define points at which decision tree splits
    splits = np.sort(np.random.uniform(x.min(), x.max(),num_splits ))
    # The value of each tree on each split is random
    values = np.random.randn(num_splits + 1)
    
    # Create piecewise constant function
    y = np.zeros_like(x)
    y[x < splits[0]] = values[0] 
    # We loop over each "split" and assign the value to value
    for i in range(num_splits - 1):
        mask = (x >= splits[i]) & (x < splits[i+1])
        y[mask] = values[i + 1]
    y[x >= splits[-1]] = values[-1]
    
    return y

# Plot
x = np.linspace(0, 1, 500)
fig, ax = subplots(figsize=(12,6))

# Create 30 random tree ensembles, average trees together like XGBoost
for i in range(30):
    
    y = sum(random_tree(x, num_splits=4) for _ in range(10))
    
    alpha = 0.2
    if i==29:
        alpha = 1.0
    ax.plot(x, y, 'r-', alpha=alpha, linewidth=4)

ax.set_title('')
ax.set_xlabel('')
ax.set_ylabel('')

ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

fig.patch.set_facecolor('black')

ax.patch.set_facecolor('black')

fig.savefig("../../images/trees.png")
