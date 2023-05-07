<template>
    <a-spin :spinning="spinning">
        <a-list v-if="comments.length" :data-source="comments"
            :header="`${comments.length} ${comments.length > 1 ? 'replies' : 'reply'}`" item-layout="horizontal">
            <template #renderItem="{ item }">
                <a-list-item>
                    <a-comment :author="item.author" :avatar="item.avatar">
                        <template #actions>
                            <span v-for="(action, index) in item.actions" :key="index">{{ action }}</span>
                        </template>
                        <template #content>
                            <MdEditor v-model="item.content" previewOnly />
                        </template>
                        <template #datetime>
                            <span>{{ item.datetime }}</span>
                        </template>
                    </a-comment>
                </a-list-item>
            </template>
        </a-list>
    </a-spin>
    <a-comment>
        <template #avatar>
            <a-avatar src="/assets/user.png" alt="User" />
        </template>
        <template #content>
            <a-form-item>
                <a-textarea v-model:value="value" :rows="4" />
            </a-form-item>
            <a-form-item>
                <a-button html-type="submit" :loading="submitting" type="primary" @click="handleSubmit">
                    提交
                </a-button>
            </a-form-item>
            <div>
                <a-radio-group v-model:value="value2" button-style="solid" style="    display: flex;
    justify-content: center;">
        <a-radio-button value="a" @click="changeStyle('creative')">创造</a-radio-button>
        <a-radio-button value="b" @click="changeStyle('balanced')">平衡</a-radio-button>
        <a-radio-button value="c" @click="changeStyle('precise')">精准</a-radio-button>
      </a-radio-group>
            </div>
            <a-button type="primary" @click="showModal">修改token</a-button>
                <a-modal v-model:open="open" title="修改token" @ok="handleOk">
                    <a-textarea v-model:value="value1" placeholder="你的token" :rows="4" />
                </a-modal>
        </template>
    </a-comment>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import dayjs from 'dayjs';
import axios, { AxiosError, AxiosResponse } from "axios"
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);
import MdEditor from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
type Comment = Record<string, string>;
import { message, Spin, Comment, List, ListItem, Avatar, Textarea, Form, Button, Modal, FormItem ,RadioGroup,RadioButton} from 'ant-design-vue';
import "ant-design-vue/es/message/style"
const child = ref(null)

export default defineComponent({
    async mounted() {
        if (window.localStorage.getItem("ai_session") == null) {
            message.error("未配置token!")
        }
    },
    components: {
        MdEditor,
        ASpin: Spin,
        AList: List,
        AComment: Comment,
        AButton: Button,
        AListItem: ListItem,
        AAvatar: Avatar,
        ATextarea: Textarea,
        AForm: Form,
        AModal: Modal,
        AFormItem: FormItem,
        ARadioButton: RadioButton,
        ARadioGroup: RadioGroup
    },
    methods: {
        async handleOk() {
            let data = [
                {
                    "name": "_U",
                    "value": this.value1
                }
            ]
            try {
                let chat = await axios.post("/api/newchat", {
                    "cookie": data,
                    "style": "balanced"
                })
                window.localStorage.setItem("ai_session", JSON.stringify(chat.data))
                this.chat_data = chat.data;
            } catch (error: any) {
                message.error(error.message)
            }
            this.open = false;
        },
        handleSubmit() {
            if (!this.value) {
                return;
            }

            this.submitting = true;

            setTimeout(() => {
                this.submitting = false;
                this.comments = [
                    ...this.comments,
                    {
                        author: 'User',
                        avatar: '/assets/user.png',
                        content: this.value,
                        datetime: dayjs().fromNow(),
                    },
                ];
                this.value = '';
            }, 0);
            this.ws.send(JSON.stringify({ "id": this.chat_data["id"], "message": this.value }))
            //ws.send(value.value);
            //ws.send({"id": })
        },
        async changeStyle(style: string) {
            try {
                let response = await axios.post("/api/change_style", {
                "id": this.chat_data["id"],
                "style": style
            })
            message.success(`成功切换对话风格:${style}`)
            } catch (error: any) {
                message.error(error.message)
            }
        }
    },
    setup() {
        const open = ref<boolean>(false);
        const value1 = ref<string>('');
        const showModal = () => {
            open.value = true;
        };
        let value2 = ref<string>('b');
        const spinning = ref<boolean>(false);
        const comments = ref<Comment[]>([]);
        const submitting = ref<boolean>(false);
        const value = ref<string>('');
        let token = ref(null)
        let nowchat = 0;
        let chat_data: any = null
        const load = message.loading("正在连接服务器", 0)
        /*let token = window.localStorage.getItem("token")
        let chat = await axios.post("/api/newchat", {
            "cookie": token,
            "style": "balanced"
        })*/
        let location = window.location.host
        let protocol = ""
        if (window.location.protocol == "https:") {
            protocol = "wss://"
        } else {
            protocol = "ws://"
        }
        let ws = new WebSocket(`${protocol}${location}/api/ws`);
        chat_data = window.localStorage.getItem("ai_session")
        ws.onopen = function(){
            load()
            message.success("成功连接服务器")
        }
        ws.onmessage = function (event) {
            if (event.data == "Websocket OK") {
                nowchat = comments.value.length
                comments.value = [
                    ...comments.value,
                    {
                        author: 'Bing',
                        avatar: '/assets/bing.svg',
                        content: "接受到请求,AI正在思考......🤔",
                        datetime: dayjs().fromNow(),
                    },
                ];
            } else {
                comments.value[nowchat] = {
                    author: 'Bing',
                    avatar: '/assets/bing.svg',
                    content: event.data,
                    datetime: dayjs().fromNow(),
                }
            }
        };
        ws.onclose = function(){
            message.warning("Websocket链接已关闭,请刷新页面")
        }
        ws.onerror = function(){
            message.warning("Websocket链接出现错误,请刷新页面")
        }
        return {
            comments,
            submitting,
            value,
            token,
            open,
            showModal,
            value1,
            chat_data,
            spinning,
            nowchat,
            ws,
            value2
        };
    },
});
</script>
  
  
