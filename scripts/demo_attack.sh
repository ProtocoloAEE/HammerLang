#!/bin/bash
chmod +w specs/bank_lcr.hml
sed -i 's/30d/20d/g' specs/bank_lcr.hml
echo "⚠️  Regla modificada: 30d → 20d"
echo "Ahora validate_locked debe FALLAR"
