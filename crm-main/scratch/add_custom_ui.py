import re

with open('frontend/src/pages/CallLogs.vue', 'r') as f:
    content = f.read()

custom_html = """
  <div 
    v-if="callLogs.data"
    class="mx-5 mb-4 p-4 bg-white/70 dark:bg-gray-900/70 backdrop-blur-md border border-gray-100 dark:border-gray-800 rounded-xl flex flex-wrap items-center justify-between gap-4 shadow-sm transition-all duration-300"
  >
    <!-- Left Side: Quick Filters -->
    <div class="flex flex-wrap items-center gap-6">
      <!-- Direction Filter -->
      <div class="flex flex-col gap-1.5">
        <span class="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">{{ __('Direction') }}</span>
        <div class="flex bg-gray-100/80 dark:bg-gray-800/80 p-0.5 rounded-lg border border-gray-200/40 dark:border-gray-700/40">
          <button 
            v-for="dir in ['all', 'inbound', 'outbound']" 
            :key="dir"
            @click="setDirectionFilter(dir)"
            :class="[
              'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200 capitalize',
              activeDirection === dir 
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' 
                : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
            ]"
          >
            {{ __(dir) }}
          </button>
        </div>
      </div>

      <!-- Flags Filter -->
      <div class="flex flex-col gap-1.5 min-w-[160px]">
        <span class="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">{{ __('Filter by Flag') }}</span>
        <select 
          :value="activeFlag"
          @change="setFlagFilter($event.target.value)"
          class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
        >
          <option value="">{{ __('All Flags') }}</option>
          <option v-for="flag in uniqueFlags" :key="flag" :value="flag">{{ flag }}</option>
        </select>
      </div>
    </div>

    <!-- Right Side: Quick Sort -->
    <div class="flex items-center gap-6">
      <!-- Sort By Field -->
      <div class="flex flex-col gap-1.5">
        <span class="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">{{ __('Sort By') }}</span>
        <div class="flex items-center gap-2">
          <div class="flex bg-gray-100/80 dark:bg-gray-800/80 p-0.5 rounded-lg border border-gray-200/40 dark:border-gray-700/40">
            <button 
              v-for="s in [
                { label: 'Date', field: 'call_date' },
                { label: 'Name', field: 'lead_name' }
              ]" 
              :key="s.field"
              @click="setSortField(s.field)"
              :class="[
                'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                activeSortField === s.field 
                  ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
              ]"
            >
              {{ __(s.label) }}
            </button>
          </div>
          <button 
            @click="toggleSortDirection"
            class="p-1.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-lg border border-gray-200/40 dark:border-gray-700/40 transition-all duration-200 flex items-center justify-center"
            :title="activeSortDirection === 'asc' ? __('Ascending') : __('Descending')"
          >
            <component 
              :is="activeSortDirection === 'asc' ? AscendingIcon : DesendingIcon" 
              class="h-4 w-4 text-gray-600 dark:text-gray-400"
            />
          </button>
        </div>
      </div>
    </div>
  </div>"""

custom_js = """
// Quick Filters and Sorts logic
import { createResource } from 'frappe-ui'
import AscendingIcon from '@/components/Icons/AscendingIcon.vue'
import DesendingIcon from '@/components/Icons/DesendingIcon.vue'

const uniqueFlagsResource = createResource({
  url: 'crm.api.doc.get_unique_flags',
  auto: true,
})
const uniqueFlags = computed(() => uniqueFlagsResource.data || [])

const activeDirection = computed(() => {
  return callLogs.value?.params?.filters?.direction || 'all'
})

function setDirectionFilter(dir) {
  let currentFilters = { ...callLogs.value.params.filters }
  if (dir && dir !== 'all') {
    currentFilters.direction = dir
  } else {
    delete currentFilters.direction
  }
  viewControls.value.updateFilter(currentFilters)
}

const activeFlag = computed(() => {
  return callLogs.value?.params?.filters?.call_flag || ''
})

function setFlagFilter(flag) {
  let currentFilters = { ...callLogs.value.params.filters }
  if (flag) {
    currentFilters.call_flag = flag
  } else {
    delete currentFilters.call_flag
  }
  viewControls.value.updateFilter(currentFilters)
}

const activeSortField = computed(() => {
  const orderBy = callLogs.value?.params?.order_by || ''
  if (orderBy.includes('lead_name')) return 'lead_name'
  if (orderBy.includes('call_date')) return 'call_date'
  return ''
})

const activeSortDirection = computed(() => {
  const orderBy = callLogs.value?.params?.order_by || ''
  if (orderBy.includes('asc')) return 'asc'
  return 'desc'
})

function setSortField(field) {
  let direction = activeSortDirection.value
  let orderBy = ''
  if (field === 'call_date') {
    orderBy = direction === 'asc' 
      ? 'call_date is null desc, call_date asc, call_time asc' 
      : 'call_date is null asc, call_date desc, call_time desc'
  } else if (field === 'lead_name') {
    orderBy = `lead_name ${direction}`
  }
  viewControls.value.updateSort(orderBy)
}

function toggleSortDirection() {
  let field = activeSortField.value || 'call_date'
  let nextDirection = activeSortDirection.value === 'asc' ? 'desc' : 'asc'
  let orderBy = ''
  if (field === 'call_date') {
    orderBy = nextDirection === 'asc' 
      ? 'call_date is null desc, call_date asc, call_time asc' 
      : 'call_date is null asc, call_date desc, call_time desc'
  } else if (field === 'lead_name') {
    orderBy = `lead_name ${nextDirection}`
  }
  viewControls.value.updateSort(orderBy)
}
"""

if '<div \n    v-if="callLogs.data"\n    class="mx-5 mb-4 p-4' not in content:
    content = content.replace('  <CallLogsListView', custom_html + '\n  <CallLogsListView')

if 'const uniqueFlagsResource = createResource' not in content:
    content = content.replace('</script>', custom_js + '\n</script>')

if 'import AscendingIcon' not in content:
    content = content.replace('import RefreshIcon', 'import RefreshIcon from \'@/components/Icons/RefreshIcon.vue\'\nimport AscendingIcon from \'@/components/Icons/AscendingIcon.vue\'\nimport DesendingIcon from \'@/components/Icons/DesendingIcon.vue\'\nimport { createResource } from \'frappe-ui\'')
    # clean up the duplicate import added in custom_js
    content = content.replace("import { createResource } from 'frappe-ui'\nimport AscendingIcon from '@/components/Icons/AscendingIcon.vue'\nimport DesendingIcon from '@/components/Icons/DesendingIcon.vue'", '')


# Add hideFilterButton back to ViewControls
view_controls = """  <ViewControls
    ref="viewControls"
    v-model="callLogs"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="CRM Call Log"
    :options="{
      hideFilterButton: true,
      hideSortButton: true,
    }"
  />"""

content = re.sub(r'  <ViewControls[\s\S]*?doctype="CRM Call Log"\n  />', view_controls, content)


with open('frontend/src/pages/CallLogs.vue', 'w') as f:
    f.write(content)
print("Updated CallLogs.vue")
