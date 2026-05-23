<template>
  <ToolPage module="to-ico" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">包含尺寸</span>
        <el-checkbox-group v-model="params.sizes">
          <el-checkbox label="16">16×16</el-checkbox>
          <el-checkbox label="32">32×32</el-checkbox>
          <el-checkbox label="48">48×48</el-checkbox>
          <el-checkbox label="64">64×64</el-checkbox>
          <el-checkbox label="128">128×128</el-checkbox>
          <el-checkbox label="256">256×256</el-checkbox>
        </el-checkbox-group>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ sizes: ['16', '32', '48', '64', '128', '256'] })
</script>

<style scoped>
.param-row { display: flex; align-items: flex-start; gap: 12px; }
.param-label { font-weight: 600; font-size: 14px; min-width: 70px; padding-top: 2px; }
</style>
