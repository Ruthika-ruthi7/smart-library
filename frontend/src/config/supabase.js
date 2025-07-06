import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://vbynfcvastgwzusnfqun.supabase.co'
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'your_supabase_anon_key_here'

export const supabase = createClient(supabaseUrl, supabaseKey)

export default supabase
