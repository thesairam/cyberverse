<template>
  <div class="h-screen flex flex-col bg-cyber-900 text-gray-100 font-mono overflow-hidden">

    <!-- ═══ TOP BAR ═══ -->
    <header class="h-10 bg-cyber-800 border-b border-cyber-600 flex items-center px-3 gap-3 flex-shrink-0">
      <div class="flex items-center gap-2">
        <div class="w-6 h-6 rounded bg-cyber-accent/20 flex items-center justify-center relative">
          <Shield class="w-4 h-4 text-cyber-accent" />
          <span class="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 bg-cyber-green rounded-full animate-pulse-slow" />
        </div>
        <span class="text-xs font-bold text-cyber-accent tracking-widest uppercase">CYBERVERSE</span>
      </div>
      <div class="flex-1 max-w-sm mx-4">
        <div class="relative">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-500" />
          <input v-model="searchQuery" @keyup.enter="doSearch" type="text" placeholder="Search..."
            class="w-full bg-cyber-700 border border-cyber-600 rounded pl-8 pr-3 py-1 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-cyber-accent/60" />
        </div>
      </div>
      <div class="flex items-center gap-3 ml-auto">
        <button @click="refreshAll" class="p-1.5 rounded hover:bg-cyber-700 text-gray-400 hover:text-cyber-accent transition-colors" title="Refresh All">
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': refreshing }" />
        </button>
        <span class="text-xs text-gray-500 font-mono hidden sm:block">{{ utcClock }}</span>
        <div class="flex items-center gap-1">
          <span class="w-1.5 h-1.5 bg-cyber-green rounded-full animate-pulse-slow" />
          <span class="text-xs text-cyber-green">LIVE</span>
        </div>
      </div>
    </header>

    <!-- ═══ MAIN GRID ═══ -->
    <div class="flex-1 flex flex-col overflow-hidden min-h-0">

      <!-- ROW 0: KPI TICKER BAR -->
      <div class="bg-cyber-900 border-b border-cyber-600 px-3 py-1.5 flex items-center gap-4 overflow-x-auto scrollbar-thin flex-shrink-0">
        <div class="flex items-center gap-1.5 text-xs whitespace-nowrap">
          <Newspaper class="w-3 h-3 text-blue-400" />
          <span class="text-gray-500">Events</span>
          <span class="text-white font-bold">{{ intelStore.stats?.total ?? '—' }}</span>
        </div>
        <div class="w-px h-4 bg-cyber-600" />
        <div class="flex items-center gap-1.5 text-xs whitespace-nowrap">
          <ShieldAlert class="w-3 h-3 text-red-400" />
          <span class="text-gray-500">Critical CVEs</span>
          <span class="text-white font-bold">{{ threatStore.critical.length }}</span>
        </div>
        <div class="w-px h-4 bg-cyber-600" />
        <div class="flex items-center gap-1.5 text-xs whitespace-nowrap">
          <TrendingUp class="w-3 h-3 text-yellow-400" />
          <span class="text-gray-500">Stocks</span>
          <span class="text-white font-bold">{{ finStore.snapshots.length }}</span>
        </div>
        <div class="w-px h-4 bg-cyber-600" />
        <div class="flex items-center gap-1.5 text-xs whitespace-nowrap">
          <Radio class="w-3 h-3 text-cyber-green" />
          <span class="text-gray-500">Live</span>
          <span class="text-white font-bold">{{ streamStore.streams.filter(s => s.is_live).length }}</span>
        </div>
        <div class="w-px h-4 bg-cyber-600" />
        <!-- Stock ticker tape -->
        <div class="flex items-center gap-3 overflow-x-auto">
          <span v-for="s in finStore.snapshots.slice(0, 10)" :key="s.ticker"
            class="flex items-center gap-1 text-xs whitespace-nowrap">
            <span class="text-gray-400 font-bold">{{ s.ticker }}</span>
            <span class="text-white">${{ s.price?.toFixed(2) ?? '—' }}</span>
            <span :class="(s.change_pct ?? 0) >= 0 ? 'text-cyber-green' : 'text-cyber-red'" class="font-bold">
              {{ (s.change_pct ?? 0) >= 0 ? '+' : '' }}{{ (s.change_pct ?? 0).toFixed(2) }}%
            </span>
          </span>
        </div>
      </div>

      <!-- ROW 1: DASHBOARD HIGHLIGHTS -->
      <div class="flex border-b border-cyber-600" style="flex:3 1 0%;min-height:0">

        <!-- Top Impact Events -->
        <div class="flex-[2] bg-cyber-900 flex flex-col overflow-hidden min-h-0 border-r border-cyber-600">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-orange-400 uppercase tracking-wider flex items-center gap-1.5">
              <Zap class="w-3 h-3" /> Top Impact
            </span>
            <span class="text-xs text-gray-600">top 10</span>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-1 min-h-0">
            <a v-for="ev in intelStore.topEvents" :key="ev.id"
              :href="ev.source_url" target="_blank" rel="noopener"
              class="flex items-start gap-2 p-1.5 rounded-lg hover:bg-cyber-700/60 transition-all group">
              <span class="text-xs font-bold flex-shrink-0 w-7 text-center rounded py-0.5"
                :class="ev.impact_score >= 7 ? 'bg-red-500/20 text-red-400' : ev.impact_score >= 4 ? 'bg-yellow-500/20 text-yellow-400' : 'bg-gray-700 text-gray-400'">
                {{ ev.impact_score.toFixed(1) }}
              </span>
              <div class="flex-1 min-w-0">
                <h4 class="text-xs text-gray-200 group-hover:text-cyber-accent transition-colors line-clamp-1">{{ ev.title }}</h4>
                <span class="text-[10px] text-gray-500">{{ ev.source_name }}</span>
              </div>
            </a>
            <div v-if="!intelStore.topEvents.length" class="text-center py-4 text-gray-600 text-xs">No data</div>
          </div>
        </div>

        <!-- Critical CVEs -->
        <div class="flex-[1] bg-cyber-900 flex flex-col overflow-hidden min-h-0 border-r border-cyber-600">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-red-400 uppercase tracking-wider flex items-center gap-1.5">
              <ShieldAlert class="w-3 h-3" /> Critical CVEs
            </span>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-1 min-h-0">
            <div v-for="t in threatStore.critical" :key="t.id"
              class="flex items-start gap-2 p-1.5 rounded-lg hover:bg-cyber-700/60 transition-all">
              <ThreatBadge :severity="t.severity" :cvss="t.cvss_score ?? undefined" />
              <div class="flex-1 min-w-0">
                <span class="text-xs text-cyber-accent font-mono">{{ t.indicator_id }}</span>
                <p class="text-[10px] text-gray-400 line-clamp-1">{{ t.title }}</p>
              </div>
            </div>
            <div v-if="!threatStore.critical.length" class="text-center py-4 text-gray-600 text-xs">No critical CVEs</div>
          </div>
        </div>

        <!-- Market Movers + Stats -->
        <div class="flex-[1] bg-cyber-900 flex flex-col overflow-hidden min-h-0">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-yellow-400 uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp class="w-3 h-3" /> Movers & Stats
            </span>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 min-h-0">
            <!-- Gainers -->
            <div class="mb-2">
              <span class="text-[10px] text-cyber-green uppercase tracking-wider font-bold">Gainers</span>
              <div v-for="s in finStore.gainers.slice(0, 3)" :key="'g-'+s.ticker"
                class="flex items-center justify-between py-0.5 text-xs">
                <span class="font-mono font-bold text-gray-300">{{ s.ticker }}</span>
                <span class="text-cyber-green font-mono font-bold">+{{ (s.change_pct ?? 0).toFixed(2) }}%</span>
              </div>
            </div>
            <!-- Losers -->
            <div class="mb-2">
              <span class="text-[10px] text-cyber-red uppercase tracking-wider font-bold">Losers</span>
              <div v-for="s in finStore.losers.slice(0, 3)" :key="'l-'+s.ticker"
                class="flex items-center justify-between py-0.5 text-xs">
                <span class="font-mono font-bold text-gray-300">{{ s.ticker }}</span>
                <span class="text-cyber-red font-mono font-bold">{{ (s.change_pct ?? 0).toFixed(2) }}%</span>
              </div>
            </div>
            <!-- Event Type Breakdown -->
            <div>
              <span class="text-[10px] text-gray-500 uppercase tracking-wider font-bold">By Type</span>
              <div v-if="intelStore.stats?.by_type" class="space-y-0.5 mt-0.5">
                <div v-for="(count, type) in intelStore.stats.by_type" :key="type"
                  class="flex items-center justify-between text-xs">
                  <span class="text-gray-400">{{ type }}</span>
                  <span class="text-white font-mono font-bold">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ROW 1: DASHBOARD HIGHLIGHTS -->
      <div class="flex border-b border-cyber-600" style="flex:3 1 0%;min-height:0">

        <!-- Top Impact Events -->
        <div class="flex-[2] bg-cyber-900 flex flex-col overflow-hidden min-h-0 border-r border-cyber-600">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-orange-400 uppercase tracking-wider flex items-center gap-1.5">
              <Zap class="w-3 h-3" /> Top Impact
            </span>
            <span class="text-xs text-gray-600">top 10</span>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-1 min-h-0">
            <a v-for="ev in intelStore.topEvents" :key="ev.id"
              :href="ev.source_url" target="_blank" rel="noopener"
              class="flex items-start gap-2 p-1.5 rounded-lg hover:bg-cyber-700/60 transition-all group">
              <span class="text-xs font-bold flex-shrink-0 w-7 text-center rounded py-0.5"
                :class="ev.impact_score >= 7 ? 'bg-red-500/20 text-red-400' : ev.impact_score >= 4 ? 'bg-yellow-500/20 text-yellow-400' : 'bg-gray-700 text-gray-400'">
                {{ ev.impact_score.toFixed(1) }}
              </span>
              <div class="flex-1 min-w-0">
                <h4 class="text-xs text-gray-200 group-hover:text-cyber-accent transition-colors line-clamp-1">{{ ev.title }}</h4>
                <span class="text-[10px] text-gray-500">{{ ev.source_name }}</span>
              </div>
            </a>
            <div v-if="!intelStore.topEvents.length" class="text-center py-4 text-gray-600 text-xs">No data</div>
          </div>
        </div>

        <!-- Critical CVEs -->
        <div class="flex-[1] bg-cyber-900 flex flex-col overflow-hidden min-h-0 border-r border-cyber-600">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-red-400 uppercase tracking-wider flex items-center gap-1.5">
              <ShieldAlert class="w-3 h-3" /> Critical CVEs
            </span>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-1 min-h-0">
            <div v-for="t in threatStore.critical" :key="t.id"
              class="flex items-start gap-2 p-1.5 rounded-lg hover:bg-cyber-700/60 transition-all">
              <ThreatBadge :severity="t.severity" :cvss="t.cvss_score ?? undefined" />
              <div class="flex-1 min-w-0">
                <span class="text-xs text-cyber-accent font-mono">{{ t.indicator_id }}</span>
                <p class="text-[10px] text-gray-400 line-clamp-1">{{ t.title }}</p>
              </div>
            </div>
            <div v-if="!threatStore.critical.length" class="text-center py-4 text-gray-600 text-xs">No critical CVEs</div>
          </div>
        </div>

        <!-- Market Movers + Stats -->
        <div class="flex-[1] bg-cyber-900 flex flex-col overflow-hidden min-h-0">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-yellow-400 uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp class="w-3 h-3" /> Movers & Stats
            </span>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 min-h-0">
            <!-- Gainers -->
            <div class="mb-2">
              <span class="text-[10px] text-cyber-green uppercase tracking-wider font-bold">Gainers</span>
              <div v-for="s in finStore.gainers.slice(0, 3)" :key="'g-'+s.ticker"
                class="flex items-center justify-between py-0.5 text-xs">
                <span class="font-mono font-bold text-gray-300">{{ s.ticker }}</span>
                <span class="text-cyber-green font-mono font-bold">+{{ (s.change_pct ?? 0).toFixed(2) }}%</span>
              </div>
            </div>
            <!-- Losers -->
            <div class="mb-2">
              <span class="text-[10px] text-cyber-red uppercase tracking-wider font-bold">Losers</span>
              <div v-for="s in finStore.losers.slice(0, 3)" :key="'l-'+s.ticker"
                class="flex items-center justify-between py-0.5 text-xs">
                <span class="font-mono font-bold text-gray-300">{{ s.ticker }}</span>
                <span class="text-cyber-red font-mono font-bold">{{ (s.change_pct ?? 0).toFixed(2) }}%</span>
              </div>
            </div>
            <!-- Event Type Breakdown -->
            <div>
              <span class="text-[10px] text-gray-500 uppercase tracking-wider font-bold">By Type</span>
              <div v-if="intelStore.stats?.by_type" class="space-y-0.5 mt-0.5">
                <div v-for="(count, type) in intelStore.stats.by_type" :key="type"
                  class="flex items-center justify-between text-xs">
                  <span class="text-gray-400">{{ type }}</span>
                  <span class="text-white font-mono font-bold">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ROW 2: MAP -->
      <div class="bg-cyber-900 flex flex-col overflow-hidden border-b border-cyber-600" style="flex:2.5 1 0%;min-height:0">
        <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
          <span class="text-xs font-bold text-cyber-accent uppercase tracking-wider flex items-center gap-1.5">
            <Globe class="w-3 h-3" /> Global Threat Map
          </span>
          <span class="text-xs text-gray-600">{{ intelStore.mapEvents.length }} events plotted</span>
        </div>
        <div class="flex-1 min-h-0">
          <WorldMap :events="intelStore.mapEvents" class="w-full h-full" />
        </div>
      </div>

      <!-- ROW 3: Intel Feed + Threat Intel -->
      <div class="flex border-b border-cyber-600" style="flex:3.5 1 0%;min-height:0">
        <!-- Intel Feed Panel -->
        <div class="flex-[3] bg-cyber-900 flex flex-col overflow-hidden min-h-0 border-r border-cyber-600">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-cyber-accent uppercase tracking-wider flex items-center gap-1.5">
              <Newspaper class="w-3 h-3" /> Intelligence Feed
            </span>
            <div class="flex items-center gap-2">
              <select v-model="intelType" @change="reloadIntel"
                class="bg-cyber-700 border border-cyber-600 rounded px-2 py-0.5 text-xs text-gray-300">
                <option value="">All</option>
                <option v-for="t in eventTypes" :key="t" :value="t">{{ t }}</option>
              </select>
              <span class="text-xs text-gray-600">{{ intelStore.total }} from {{ intelStore.sources.length }} sources</span>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-1.5 min-h-0">
            <a v-for="ev in intelStore.events" :key="ev.id"
              :href="ev.source_url" target="_blank" rel="noopener"
              class="block p-2 rounded-lg bg-cyber-800/50 hover:bg-cyber-700/60 border border-transparent hover:border-cyber-accent/20 transition-all group">
              <div class="flex items-start justify-between gap-2">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-1.5 mb-0.5">
                    <EventTypeBadge :type="ev.event_type" />
                    <span class="text-xs text-gray-500">{{ ev.source_name }}</span>
                    <span v-if="ev.country" class="text-xs text-gray-600">· {{ ev.country }}</span>
                  </div>
                  <h3 class="text-xs text-gray-200 group-hover:text-cyber-accent transition-colors line-clamp-2">{{ ev.title }}</h3>
                </div>
                <span class="text-xs font-bold flex-shrink-0"
                  :class="ev.impact_score >= 7 ? 'text-red-400' : ev.impact_score >= 4 ? 'text-yellow-400' : 'text-gray-500'">
                  {{ ev.impact_score.toFixed(1) }}
                </span>
              </div>
            </a>
            <div v-if="!intelStore.events.length" class="text-center py-6 text-gray-600 text-xs">No events found</div>
          </div>
          <div class="flex items-center justify-center gap-2 px-3 py-1 border-t border-cyber-600 flex-shrink-0">
            <button @click="intelPrev" :disabled="intelStore.page === 1" class="px-2 py-0.5 text-xs rounded bg-cyber-700 text-gray-400 disabled:opacity-30">‹</button>
            <span class="text-xs text-gray-500">{{ intelStore.page }} / {{ intelStore.totalPages || 1 }}</span>
            <button @click="intelNext" :disabled="intelStore.page >= intelStore.totalPages" class="px-2 py-0.5 text-xs rounded bg-cyber-700 text-gray-400 disabled:opacity-30">›</button>
          </div>
        </div>

        <!-- Threat Intel Panel -->
        <div class="flex-[2] bg-cyber-900 flex flex-col overflow-hidden min-h-0">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-red-400 uppercase tracking-wider flex items-center gap-1.5">
              <ShieldAlert class="w-3 h-3" /> Threat Intel
            </span>
            <select v-model="threatSeverity" @change="reloadThreats"
              class="bg-cyber-700 border border-cyber-600 rounded px-2 py-0.5 text-xs text-gray-300">
              <option value="">All</option>
              <option v-for="s in severities" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin min-h-0">
            <table class="w-full text-xs">
              <thead class="text-gray-500 uppercase border-b border-cyber-600 sticky top-0 bg-cyber-900 z-10">
                <tr>
                  <th class="py-1 px-2 text-left">CVE</th>
                  <th class="py-1 px-2 text-left">Sev</th>
                  <th class="py-1 px-2 text-left">CVSS</th>
                  <th class="py-1 px-2 text-left">Title</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-cyber-700/50">
                <tr v-for="t in threatStore.threats" :key="t.id" class="hover:bg-cyber-700/40 transition-colors">
                  <td class="py-1 px-2 font-mono text-cyber-accent whitespace-nowrap">{{ t.indicator_id }}</td>
                  <td class="py-1 px-2"><ThreatBadge :severity="t.severity" /></td>
                  <td class="py-1 px-2 font-mono" :class="cvssColor(t.cvss_score)">{{ t.cvss_score?.toFixed(1) ?? '—' }}</td>
                  <td class="py-1 px-2 text-gray-300 truncate max-w-[200px]">{{ t.title }}</td>
                </tr>
                <tr v-if="!threatStore.threats.length"><td colspan="4" class="py-4 text-center text-gray-600">No threats</td></tr>
              </tbody>
            </table>
          </div>
          <div class="flex items-center justify-center gap-2 px-3 py-1 border-t border-cyber-600 flex-shrink-0">
            <button @click="threatPrev" :disabled="threatStore.page === 1" class="px-2 py-0.5 text-xs rounded bg-cyber-700 text-gray-400 disabled:opacity-30">‹</button>
            <span class="text-xs text-gray-500">{{ threatStore.page }}</span>
            <button @click="threatNext" :disabled="threatStore.total <= threatStore.page * 20" class="px-2 py-0.5 text-xs rounded bg-cyber-700 text-gray-400 disabled:opacity-30">›</button>
          </div>
        </div>
      </div>

      <!-- ROW 4: Streams + Financial + Certs -->
      <div class="flex" style="flex:2.5 1 0%;min-height:0">
        <!-- Live Streams Panel -->
        <div class="flex-1 bg-cyber-900 flex flex-col overflow-hidden min-h-0 border-r border-cyber-600">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-cyber-green uppercase tracking-wider flex items-center gap-1.5">
              <Radio class="w-3 h-3" /> Streams
            </span>
            <label class="flex items-center gap-1 text-xs text-gray-400 cursor-pointer">
              <input type="checkbox" v-model="liveOnly" @change="loadStreams" class="accent-cyber-green w-3 h-3" />
              Live
            </label>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-1.5 min-h-0">
            <a v-for="s in streamStore.streams" :key="s.video_id"
              :href="s.stream_url" target="_blank" rel="noopener"
              class="block p-2 rounded-lg bg-cyber-800/50 hover:bg-cyber-700/60 border border-transparent hover:border-cyber-green/20 transition-all group">
              <div class="flex gap-2">
                <div class="relative w-20 h-12 flex-shrink-0 rounded overflow-hidden bg-cyber-700">
                  <img v-if="s.thumbnail_url" :src="s.thumbnail_url" :alt="s.title" class="w-full h-full object-cover" />
                  <span v-if="s.is_live" class="absolute top-0.5 left-0.5 bg-red-600 text-white text-[9px] px-1 rounded font-bold">LIVE</span>
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-xs text-gray-200 group-hover:text-cyber-green transition-colors line-clamp-2 leading-tight">{{ s.title }}</h3>
                  <div class="flex items-center gap-2 mt-0.5 text-[10px] text-gray-500">
                    <span>{{ s.channel_name }}</span>
                    <span v-if="s.viewer_count">👁 {{ s.viewer_count.toLocaleString() }}</span>
                  </div>
                </div>
              </div>
            </a>
            <div v-if="!streamStore.streams.length" class="text-center py-6 text-gray-600 text-xs">No streams</div>
          </div>
        </div>

        <!-- Financial Panel -->
        <div class="flex-1 bg-cyber-900 flex flex-col overflow-hidden min-h-0 border-r border-cyber-600">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-yellow-400 uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp class="w-3 h-3" /> Financial
            </span>
            <div class="flex gap-1">
              <button v-for="s in ['', 'cybersecurity', 'ai']" :key="s" @click="filterSector(s)"
                :class="['px-1.5 py-0.5 text-[10px] rounded transition-colors',
                  activeSector === s ? 'bg-yellow-400/20 text-yellow-400' : 'text-gray-500 hover:text-gray-300']">
                {{ s || 'All' }}
              </button>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin min-h-0">
            <table class="w-full text-xs">
              <thead class="text-gray-500 uppercase border-b border-cyber-600 sticky top-0 bg-cyber-900 z-10">
                <tr>
                  <th class="py-1 px-2 text-left">Ticker</th>
                  <th class="py-1 px-2 text-right">Price</th>
                  <th class="py-1 px-2 text-right">Chg%</th>
                  <th class="py-1 px-2 text-right">MCap</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-cyber-700/50">
                <tr v-for="s in displayedSnapshots" :key="s.ticker" class="hover:bg-cyber-700/40 transition-colors">
                  <td class="py-1 px-2">
                    <a :href="`https://finance.yahoo.com/quote/${s.ticker}`" target="_blank" rel="noopener"
                      class="font-mono font-bold text-cyber-accent hover:text-cyber-accent/80">{{ s.ticker }}</a>
                  </td>
                  <td class="py-1 px-2 text-right font-mono text-white">${{ s.price?.toFixed(2) ?? '—' }}</td>
                  <td class="py-1 px-2 text-right font-mono font-bold"
                    :class="(s.change_pct ?? 0) >= 0 ? 'text-cyber-green' : 'text-cyber-red'">
                    {{ (s.change_pct ?? 0) >= 0 ? '+' : '' }}{{ (s.change_pct ?? 0).toFixed(2) }}%
                  </td>
                  <td class="py-1 px-2 text-right text-gray-400">{{ fmtMcap(s.market_cap) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Certifications Panel -->
        <div class="flex-1 bg-cyber-900 flex flex-col overflow-hidden min-h-0">
          <div class="flex items-center justify-between px-3 py-1 border-b border-cyber-600 flex-shrink-0">
            <span class="text-xs font-bold text-purple-400 uppercase tracking-wider flex items-center gap-1.5">
              <Award class="w-3 h-3" /> Certifications
            </span>
          </div>
          <div class="flex flex-wrap gap-1 px-2 py-1 border-b border-cyber-700 flex-shrink-0">
            <button @click="filterCertBody('')" :class="certBtnClass('')" class="text-[10px]">All</button>
            <button v-for="b in certBodies" :key="b" @click="filterCertBody(b)" :class="certBtnClass(b)" class="text-[10px]">{{ b }}</button>
          </div>
          <div class="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-1 min-h-0">
            <div v-for="c in certItems" :key="c.id"
              class="p-2 rounded-lg bg-cyber-800/50 hover:bg-cyber-700/60 border border-transparent hover:border-purple-400/20 transition-all">
              <div class="flex items-start gap-2">
                <span class="bg-purple-500/20 text-purple-400 px-1.5 py-0.5 rounded text-[10px] font-bold whitespace-nowrap flex-shrink-0">{{ c.body_name }}</span>
                <div class="flex-1 min-w-0">
                  <a v-if="c.source_url" :href="c.source_url" target="_blank"
                    class="text-xs text-gray-200 hover:text-purple-400 transition-colors line-clamp-2">{{ c.title }}</a>
                  <p v-else class="text-xs text-gray-200 line-clamp-2">{{ c.title }}</p>
                  <div class="flex items-center gap-2 mt-0.5 text-[10px] text-gray-500">
                    <span v-if="c.region">🌍 {{ c.region }}</span>
                    <span v-if="c.update_type" class="text-purple-600">{{ c.update_type }}</span>
                    <span v-if="c.published_at">{{ fmtCertDate(c.published_at) }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="!certItems.length" class="text-center py-6 text-gray-600 text-xs">No updates</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ FOOTER ═══ -->
    <footer class="h-6 bg-cyber-800 border-t border-cyber-600 flex items-center px-3 gap-4 text-[10px] text-gray-600 flex-shrink-0">
      <span>CyberVerse Intelligence Aggregator v1.0</span>
      <span class="ml-auto">GDELT · NVD · RSS · yFinance · YouTube</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { format } from 'date-fns'
import {
  Shield, Search, RefreshCw, Globe, Newspaper, ShieldAlert,
  TrendingUp, Radio, Award, Zap
} from 'lucide-vue-next'

import WorldMap from '@/components/map/WorldMap.vue'
import EventTypeBadge from '@/components/ui/EventTypeBadge.vue'
import ThreatBadge from '@/components/ui/ThreatBadge.vue'

import { useIntelligenceStore } from '@/stores/intelligence'
import { useFinancialStore } from '@/stores/financial'
import { useThreatsStore } from '@/stores/threats'
import { useStreamsStore } from '@/stores/streams'
import { certificationsApi } from '@/services/api'
import type { CertificationUpdate } from '@/types'

// ── Stores ───────────────────────────────────────────────────
const intelStore = useIntelligenceStore()
const finStore = useFinancialStore()
const threatStore = useThreatsStore()
const streamStore = useStreamsStore()

// ── Top bar state ────────────────────────────────────────────
const searchQuery = ref('')
const refreshing = ref(false)
const utcClock = ref('')
let clockInterval: ReturnType<typeof setInterval>

// ── Intel panel ──────────────────────────────────────────────
const eventTypes = ['NEWS', 'ALERT', 'POLICY', 'FINANCIAL', 'VIDEO', 'CERTIFICATION', 'STARTUP', 'PRODUCT']
const intelType = ref('')

function reloadIntel() {
  intelStore.filters.event_type = intelType.value
  intelStore.page = 1
  intelStore.fetchEvents()
}
function intelPrev() { if (intelStore.page > 1) { intelStore.page--; intelStore.fetchEvents() } }
function intelNext() { if (intelStore.page < intelStore.totalPages) { intelStore.page++; intelStore.fetchEvents() } }

// ── Threat panel ─────────────────────────────────────────────
const severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
const threatSeverity = ref('')

function reloadThreats() {
  threatStore.filters.severity = threatSeverity.value
  threatStore.page = 1
  threatStore.fetchThreats()
}
function threatPrev() { if (threatStore.page > 1) { threatStore.page--; threatStore.fetchThreats() } }
function threatNext() { threatStore.page++; threatStore.fetchThreats() }
function cvssColor(s?: number | null) {
  if (!s) return 'text-gray-500'
  if (s >= 9) return 'text-red-400'
  if (s >= 7) return 'text-orange-400'
  if (s >= 4) return 'text-yellow-400'
  return 'text-blue-400'
}

// ── Streams panel ────────────────────────────────────────────
const liveOnly = ref(false)
function loadStreams() { streamStore.fetchStreams(liveOnly.value) }

// ── Financial panel ──────────────────────────────────────────
const activeSector = ref('')
const displayedSnapshots = computed(() => {
  if (!activeSector.value) return finStore.snapshots
  return finStore.snapshots.filter(s => s.sector?.toLowerCase() === activeSector.value)
})
function filterSector(s: string) { activeSector.value = s }
function fmtMcap(v?: number | null) {
  if (!v) return '—'
  if (v >= 1e12) return (v / 1e12).toFixed(1) + 'T'
  if (v >= 1e9) return (v / 1e9).toFixed(1) + 'B'
  return (v / 1e6).toFixed(0) + 'M'
}

// ── Certifications panel ─────────────────────────────────────
const certBodies = ref<string[]>([])
const certItems = ref<CertificationUpdate[]>([])
const activeCertBody = ref('')

async function loadCerts() {
  const params: Record<string, unknown> = { page_size: 50 }
  if (activeCertBody.value) params.body_name = activeCertBody.value
  const { data } = await certificationsApi.list(params)
  certItems.value = data.items
}
async function filterCertBody(b: string) {
  activeCertBody.value = b
  await loadCerts()
}
function certBtnClass(b: string) {
  return activeCertBody.value === b
    ? 'px-1.5 py-0.5 rounded border border-purple-400 text-purple-400 bg-purple-400/10'
    : 'px-1.5 py-0.5 rounded border border-cyber-600 text-gray-500 hover:text-gray-300'
}
function fmtCertDate(d: string) {
  try { return format(new Date(d), 'MMM d, yyyy') } catch { return '—' }
}

// ── Search ───────────────────────────────────────────────────
function doSearch() {
  if (!searchQuery.value.trim()) return
  intelStore.filters.search = searchQuery.value.trim()
  intelStore.page = 1
  intelStore.fetchEvents()
}

// ── Refresh all ──────────────────────────────────────────────
async function refreshAll() {
  refreshing.value = true
  await Promise.all([
    intelStore.fetchEvents(),
    intelStore.fetchTopEvents(10),
    intelStore.fetchMapEvents(),
    intelStore.fetchStats(),
    intelStore.fetchSources(),
    finStore.fetchSnapshots(),
    finStore.fetchMovers(),
    threatStore.fetchThreats(),
    threatStore.fetchCritical(),
    streamStore.fetchStreams(liveOnly.value),
    loadCerts(),
  ])
  refreshing.value = false
}

// ── Mount ────────────────────────────────────────────────────
onMounted(async () => {
  clockInterval = setInterval(() => {
    utcClock.value = new Date().toUTCString().slice(17, 25) + ' UTC'
  }, 1000)

  // Load everything in parallel
  const certBodiesReq = certificationsApi.bodies()

  await Promise.all([
    intelStore.fetchEvents(),
    intelStore.fetchTopEvents(10),
    intelStore.fetchMapEvents(),
    intelStore.fetchStats(),
    intelStore.fetchSources(),
    finStore.fetchSnapshots(),
    finStore.fetchMovers(),
    threatStore.fetchThreats(),
    threatStore.fetchCritical(),
    streamStore.fetchStreams(),
    loadCerts(),
  ])

  const bodiesRes = await certBodiesReq
  certBodies.value = bodiesRes.data.bodies
})

onUnmounted(() => clearInterval(clockInterval))
</script>

<style scoped>
.scrollbar-thin {
  scrollbar-width: thin;
  scrollbar-color: #243044 #0d1224;
}
.scrollbar-thin::-webkit-scrollbar { width: 4px; }
.scrollbar-thin::-webkit-scrollbar-track { background: #0d1224; }
.scrollbar-thin::-webkit-scrollbar-thumb { background: #243044; border-radius: 2px; }
.scrollbar-thin::-webkit-scrollbar-thumb:hover { background: #00d8ff44; }
</style>
