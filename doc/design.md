# 需求

## 必要功能

* 登录
  
1. 支持OAuth协议登录接口（如西北大学统一身份认证，QQ登录）
2. 支持HTTP Basic Auth（预留给WebDAV）

* 文件功能细节

  ![原型图1](design/原型1.png)

  1. 能够以层级方式查看所有文件夹
  2. 能够显示文件夹中的文件
  3. 每个文件/文件夹可以下载。
  4. 每个文件/文件夹可以共享，得到共享链接。
  5. 每个文件/文件夹可以删除。
  6. 每个文件/文件夹可以重命名。
  7. 能够显示文件/文件夹的常用属性，如大小，创建时间。
  8. 有多选，全选功能。

## 可选功能

* 文件

  1. 每个可预览文件可以点击预览，如png，txt，cpp，doc，pdf。
  2. 共享可选择公开共享/私密共享
     * 公开共享：访问个人主页即可查看公开共享的文件
     * 私密共享：需得到共享链接才能查看共享的文件
  3. 搜索功能。

* 群组

  1. 群组由发起人，受邀人，群组资料库组成。
  2. 发起人可以邀请其他人进入群组。
  3. 所有人都可以向群组资料库上传文件。
  4. 所有人都可以从群组资料库下载文件。
  5. 所有人都可以在资料库新建文件夹。
  6. 发起人可以删除/重命名群组资料库所有文件。
  7. 受邀人只能删除/重命名自己上传的文件。

# 设计

* 文件夹层级信息使用树状结构保存在数据库中。<https://www.zhihu.com/question/20417447>

* 数据库设计见Models。

# 工作流

## Workflow

1. Clone master分支
2. 在本地创建development分支进行开发
3. pull origin（防止覆盖他人提交）后merge或rebase到master分支
4. push origin

## Fork Workflow（弃用）

1. 在Github上fork上游仓库

2. Clone fork下来的仓库到本地

3. 查看当前的远程仓库：

   `git remote -v`

![1573179566960](design/1573179566960.png)

​	这时只有fork后的仓库。

2. 添加一个需要同步的上游仓库：

   ` git remote add upstream git@github.com:NWU-Cloud-Storage/cloud-storage.git`

3. 确认添加成功：

   ![1573179736006](design/1573179736006.png)

4. 同步上游更改：两种方法

   * `git pull upstream`

   * ```shell
     git fetch upstream
     git checkout master # 检出至master分支
     git merge upstream/master
     ```

     两种方式的区别是pull会自动尝试merge操作，而fetch只会把上游更改保存到upstream/master分支中。

5. 本地进行开发

6. 将更改推送至fork后的仓库`git push origin`

7. 在Github上创建Pull Request