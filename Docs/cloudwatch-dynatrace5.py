import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up figure
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Add boxes and arrows
components = {
    "EC2 Instance(s)": (10, 75),
    "CloudWatch Agent": (30, 75),
    "SSM Parameter Store": (50, 90),
    "CloudWatch Logs/Metrics": (50, 75),
    "Alarms (CPU/Memory)": (70, 75),
    "Auto Scaling Group": (30, 50),
    "Scaling Policies": (50, 50),
    "SNS Topic + Email": (70, 50),
    "CloudWatch Dashboard": (50, 30)
}

for name, (x, y) in components.items():
    ax.add_patch(patches.Rectangle((x - 10, y - 5), 20, 10, edgecolor='black', facecolor='lightyellow'))
    ax.text(x, y, name, ha='center', va='center', fontsize=10, wrap=True)

# Arrows
arrows = [
    ((10, 75), (20, 75)),   # EC2 -> Agent
    ((30, 75), (40, 75)),   # Agent -> Logs/Metrics
    ((50, 90), (30, 75)),   # SSM -> Agent
    ((50, 75), (60, 75)),   # Metrics -> Alarms
    ((70, 75), (70, 60)),   # Alarms -> SNS
    ((70, 75), (50, 50)),   # Alarms -> Policies
    ((30, 75), (30, 55)),   # Agent -> ASG
    ((50, 50), (30, 50)),   # Policies -> ASG
    ((70, 50), (60, 50)),   # SNS -> Scaling
    ((50, 75), (50, 35))    # Metrics -> Dashboard
]

for start, end in arrows:
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", lw=1.5))

# Title
plt.title("Terraform-Deployed AWS EC2 + CloudWatch + Auto Scaling Architecture", fontsize=13)
diagram_path = "/mnt/data/cloudwatch_autoscaling_architecture.png"
plt.savefig(diagram_path, bbox_inches='tight')
diagram_path
Result
'/mnt/data/cloudwatch_autoscaling_architecture.png'
