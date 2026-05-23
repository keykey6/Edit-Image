<template>
  <ToolPage module="sketch-effect" :params="params">
    <template #params>
      <div class="param-group">
        <label class="param-label">风格</label>
        <el-radio-group v-model="params.style">
          <el-radio-button value="pencil">铅笔素描</el-radio-button>
          <el-radio-button value="canny">Canny 线稿</el-radio-button>
          <el-radio-button value="comic">漫画效果</el-radio-button>
        </el-radio-group>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive<Record<string, unknown>>({
  style: 'pencil',
})
</script>

<style scoped>
.param-group {
  margin-top: 4px;
}
.param-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}
</style>
