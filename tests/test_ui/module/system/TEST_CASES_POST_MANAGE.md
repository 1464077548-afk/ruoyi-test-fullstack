# 岗位管理模块测试用例清单

## 测试用例统计

| 测试类别 | 用例数量 | 优先级分布 |
|---------|---------|-----------|
| **API层测试 (L1)** | 15 | P0×5, P1×4, P2×4, P3×2 |
| **UI层测试 (L2)** | 9 | P0×4, P1×3, P2×2 |
| **集成测试 (L3)** | 2 | P0×1, P1×1 |
| **性能测试** | 2 | P1×2 |
| **安全测试** | 7 | P1×2, P2×5 |
| **批量操作测试** | 4 | P1×3, P2×1 |
| **边界场景测试** | 5 | P2×3, P3×2 |
| **总计** | **44** | |

---

## 1. API层测试 (TestPostAPI)

### 1.1 基础功能测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| API-001 | test_get_post_list_success | P0 | 获取岗位列表成功 |
| API-002 | test_create_post_success | P0 | 创建岗位成功 |
| API-003 | test_update_post_success | P0 | 更新岗位成功 |
| API-004 | test_delete_post_success | P0 | 删除岗位成功 |

### 1.2 异常场景测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| API-005 | test_create_post_duplicate_name | P1 | 创建重复岗位名称 |
| API-006 | test_create_post_duplicate_code | P1 | 创建重复岗位编码 |
| API-007 | test_delete_post_not_exists | P1 | 删除不存在的岗位 |
| API-008 | test_query_post_by_name | P1 | 根据岗位名称查询 |
| API-009 | test_create_post_missing_required_fields | P3 | 创建岗位缺少必填字段 |
| API-010 | test_create_post_too_long_name | P3 | 创建岗位名称过长 |

### 1.3 验证功能测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| API-011 | test_validate_post_name_unique | P2 | 验证岗位名称唯一性 |
| API-012 | test_validate_post_code_unique | P2 | 验证岗位编码唯一性 |
| API-013 | test_get_post_by_id | P2 | 根据ID获取岗位 |

### 1.4 高级功能测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| API-014 | test_export_posts | P2 | 导出岗位数据 |
| API-015 | test_pagination | P2 | 分页功能测试 |

---

## 2. UI层测试 (TestPostUIModule)

### 2.1 基础功能测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| UI-001 | test_post_page_load | P0 | 岗位管理页面加载 |
| UI-002 | test_create_post_success | P0 | 新增岗位成功 |
| UI-003 | test_edit_post_success | P0 | 编辑岗位成功 |
| UI-004 | test_delete_post_success | P0 | 删除岗位成功 |

### 2.2 异常场景测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| UI-005 | test_create_post_duplicate_name | P1 | 新增重复岗位名称 |
| UI-006 | test_create_post_missing_required_fields | P1 | 新增岗位缺少必填字段 |
| UI-007 | test_search_post_by_name | P1 | 按名称搜索岗位 |
| UI-008 | test_create_post_cancel | P2 | 新增岗位取消 |

### 2.3 查询功能测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| UI-009 | test_get_post_info | P2 | 获取岗位信息 |

---

## 3. 集成测试 (TestPostLifecycleE2E)

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| E2E-001 | test_complete_post_lifecycle | P0 | 完整岗位生命周期流程（创建→验证→编辑→验证→搜索→删除→验证） |
| E2E-002 | test_post_crud_operations | P1 | 岗位增删改查操作 |

---

## 4. 性能测试 (TestPostPerformance)

| 用例ID | 用例名称 | 优先级 | 测试场景 | 性能指标 |
|-------|---------|--------|---------|---------|
| PERF-001 | test_create_post_performance | P1 | 创建岗位性能测试 | 最大耗时<5s |
| PERF-002 | test_query_post_performance | P1 | 查询岗位性能测试 | 最大耗时<3s |

---

## 5. 安全测试 (TestPostSecurity)

### 5.1 注入攻击测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| SEC-001 | test_create_post_sql_injection | P1 | SQL注入测试 |
| SEC-002 | test_create_post_xss | P1 | XSS攻击测试 |

### 5.2 权限测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| SEC-003 | test_unauthorized_access | P2 | 未授权访问测试 |

### 5.3 边界值测试

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| SEC-004 | test_get_nonexistent_post | P2 | 获取不存在的岗位 |
| SEC-005 | test_delete_nonexistent_post | P2 | 删除不存在的岗位 |
| SEC-006 | test_special_characters_in_name | P2 | 特殊字符岗位名称 |
| SEC-007 | test_boundary_post_sort | P2 | 岗位排序边界值测试 |

---

## 6. 批量操作测试 (TestPostBatchOperations)

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| BATCH-001 | test_batch_delete_posts | P1 | API批量删除岗位 |
| BATCH-002 | test_change_post_status | P1 | API修改岗位状态 |
| BATCH-003 | test_toggle_post_status_ui | P1 | UI切换岗位状态 |
| BATCH-004 | test_batch_delete_posts_ui | P2 | UI批量删除岗位 |

---

## 7. 边界场景测试 (TestPostEdgeCases)

| 用例ID | 用例名称 | 优先级 | 测试场景 |
|-------|---------|--------|---------|
| EDGE-001 | test_create_post_with_emoji | P2 | 创建带Emoji的岗位名称 |
| EDGE-002 | test_create_post_empty_remark | P2 | 创建岗位备注为空 |
| EDGE-003 | test_concurrent_post_creation | P2 | 并发创建相同岗位 |
| EDGE-004 | test_query_with_special_params | P3 | 使用特殊参数查询 |
| EDGE-005 | test_invalid_pagination_params | P3 | 无效分页参数 |

---

## 测试标记说明

| 标记 | 说明 |
|-----|------|
| `@pytest.mark.api` | API层测试 |
| `@pytest.mark.ui` | UI层测试 |
| `@pytest.mark.e2e` | 端到端测试 |
| `@pytest.mark.performance` | 性能测试 |
| `@pytest.mark.security` | 安全测试 |
| `@pytest.mark.l1` | 一级测试（API层） |
| `@pytest.mark.l2` | 二级测试（UI层） |
| `@pytest.mark.l3` | 三级测试（集成/性能/安全） |
| `@pytest.mark.p0` | 核心功能，阻塞发布 |
| `@pytest.mark.p1` | 重要功能 |
| `@pytest.mark.p2` | 一般功能 |
| `@pytest.mark.p3` | 低优先级 |

---

## 测试执行指南

### 运行所有岗位管理测试
```bash
pytest tests/test_ui/module/system/test_post_manage.py -v
```

### 运行指定层级的测试
```bash
# 仅运行API测试
pytest tests/test_ui/module/system/test_post_manage.py -v -m api

# 仅运行UI测试
pytest tests/test_ui/module/system/test_post_manage.py -v -m ui

# 仅运行性能测试
pytest tests/test_ui/module/system/test_post_manage.py -v -m performance

# 仅运行安全测试
pytest tests/test_ui/module/system/test_post_manage.py -v -m security
```

### 运行指定优先级的测试
```bash
# 运行P0和P1测试
pytest tests/test_ui/module/system/test_post_manage.py -v -m "p0 or p1"

# 运行P2测试
pytest tests/test_ui/module/system/test_post_manage.py -v -m p2
```

### 并行执行测试
```bash
# 使用pytest-xdist并行执行
pytest tests/test_ui/module/system/test_post_manage.py -n auto
```

---

## 依赖文件

1. **API客户端**: `api/clients/post_client.py`
2. **UI页面**: `ui/pages/modules/post_page.py`
3. **UI业务逻辑**: `ui/biz/normal/post_biz.py`
4. **测试数据工厂**: `common/utils/data_factory.py` (generate_post_data方法)
5. **测试配置**: `tests/conftest.py` (post_client, post_biz, test_post_data fixtures)

---

## 测试数据隔离

- 所有测试数据使用工作器ID前缀（如 `gw0_`、`gw1_`）确保并行执行时数据隔离
- 测试结束后自动清理本工作器创建的测试数据
- 岗位名称格式: `{worker_id}_测试岗位_{timestamp}_{random}`
- 岗位编码格式: `{worker_id}_post_{timestamp}_{random}`
