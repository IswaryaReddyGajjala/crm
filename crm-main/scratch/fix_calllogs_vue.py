with open('frontend/src/pages/CallLogs.vue', 'r') as f:
    content = f.read()

# Remove the incorrectly placed imports at the bottom
content = content.replace("import { createResource } from 'frappe-ui'\nimport AscendingIcon from '@/components/Icons/AscendingIcon.vue'\nimport DesendingIcon from '@/components/Icons/DesendingIcon.vue'\n", "")

# Add the imports to the top of the <script setup> block
script_setup_tag = "<script setup>\n"
if "import AscendingIcon" not in content:
    content = content.replace(script_setup_tag, script_setup_tag + "import AscendingIcon from '@/components/Icons/AscendingIcon.vue'\nimport DesendingIcon from '@/components/Icons/DesendingIcon.vue'\n")

with open('frontend/src/pages/CallLogs.vue', 'w') as f:
    f.write(content)
print("Fixed CallLogs.vue imports")
