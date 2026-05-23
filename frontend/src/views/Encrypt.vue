<template>
  <ToolPage module="encrypt" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">密码</span>
        <el-input v-model="params.password" type="password" show-password placeholder="输入加密密码" size="small" style="width: 240px" />
      </div>
      <div class="param-note">
        <el-alert title="使用 AES-256-CBC 加密，解密时需要相同密码" type="info" show-icon :closable="false" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ password: '' })
</script>

<style scoped>
.param-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
.param-note { margin-top: 8px; }
</style>
