<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider breakpoint="lg" collapsed-width="0" @collapse="onCollapse" @breakpoint="onBreakpoint">
      <div class="logo"></div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item key="/">
          <home-outlined />
          <span>主页</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0" />
      <router-view></router-view>
      <a-layout-footer style="text-align: center">
        VMTask
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script lang="ts">
import {
  HomeOutlined
} from '@ant-design/icons-vue';
import { defineComponent, ref } from 'vue';
import { Breadcrumb, BreadcrumbItem, LayoutContent, Menu, MenuItem, Layout, LayoutFooter, LayoutHeader, LayoutSider } from 'ant-design-vue'
export default defineComponent({
  components: {
    HomeOutlined,
    BreadcrumbItem,
    ALayout: Layout,
    ALayoutContent: LayoutContent,
    ALayoutFooter: LayoutFooter,
    ALayoutHeader: LayoutHeader,
    ALayoutSider: LayoutSider,
    AMenu: Menu,
    AMenuItem: MenuItem,
    ABreadcrumbItem: BreadcrumbItem,
    ABreadcrumb: Breadcrumb
  },
  setup() {
    const onCollapse = (collapsed: boolean, type: string) => {
      console.log(collapsed, type);
    };

    const onBreakpoint = (broken: boolean) => {
      console.log(broken);
    };

    const selectedKeys = ref<string[]>(['/']);
    return {
      onCollapse,
      onBreakpoint,
      selectedKeys
    }
  }
});
</script>
<style>
#components-layout-demo-side .logo {
  height: 32px;
  margin: 16px;
  background: rgba(255, 255, 255, 0.3);
}

.site-layout .site-layout-background {
  background: #fff;
}

[data-theme='dark'] .site-layout .site-layout-background {
  background: #141414;
}
</style>
