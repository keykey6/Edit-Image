<template>
  <ToolPage module="social-media" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">平台</span>
        <el-select v-model="params.platform" size="small" style="width: 200px">
          <el-option label="微博 (3:2)" value="weibo" />
          <el-option label="小红书 (3:4)" value="xiaohongshu" />
          <el-option label="微信朋友圈 (1:1)" value="wechat" />
          <el-option label="Instagram (1:1)" value="instagram" />
          <el-option label="Twitter (16:9)" value="twitter" />
          <el-option label="Facebook (1.91:1)" value="facebook" />
        </el-select>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ platform: 'weibo' })
</script>

<style scoped>
.param-row { display: flex; align-items: center; gap: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
</style>
