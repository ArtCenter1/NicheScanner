# === 4. 测试 ===
echo ""
echo "==> [4/6] 运行测试"
PYTHONPATH=./backend python -m pytest backend/tests/ -v --tb=short -q 2>&1 || {
    echo "FAIL: 测试未通过"
    exit 1
}
echo "   ✅ 测试通过"