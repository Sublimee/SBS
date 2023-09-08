/*
 * Copyright (c) 1997, 2019, Oracle and/or its affiliates. All rights reserved.
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
 *
 * This code is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 2 only, as
 * published by the Free Software Foundation.  Oracle designates this
 * particular file as subject to the "Classpath" exception as provided
 * by Oracle in the LICENSE file that accompanied this code.
 *
 * This code is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * version 2 for more details (a copy is included in the LICENSE file that
 * accompanied this code).
 *
 * You should have received a copy of the GNU General Public License version
 * 2 along with this work; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * Please contact Oracle, 500 Oracle Parkway, Redwood Shores, CA 94065 USA
 * or visit www.oracle.com if you need additional information or have any
 * questions.
 */

package strong.ideas.lesson_7.after;
import java.util.AbstractCollection;
import java.util.AbstractSet;
import java.util.Collection;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

public abstract class AM<K,V> implements Map<K,V> {
    
    protected AM() {
    }

    // Query Operations

    
    public int size() {
        return entrySet().size();
    }

    
    public boolean isEmpty() {
        return size() == 0;
    }

    
    public boolean containsValue(Object value) {
        Iterator<Entry<K,V>> i = entrySet().iterator();
        if (value==null) {
            while (i.hasNext()) {
                Entry<K,V> e = i.next();
                if (e.getValue()==null)
                    return true;
            }
        } else {
            while (i.hasNext()) {
                Entry<K,V> e = i.next();
                if (value.equals(e.getValue()))
                    return true;
            }
        }
        return false;
    }

    
    public boolean containsKey(Object key) {
        Iterator<Entry<K,V>> i = entrySet().iterator();
        if (key==null) {
            while (i.hasNext()) {
                Entry<K,V> e = i.next();
                if (e.getKey()==null)
                    return true;
            }
        } else {
            while (i.hasNext()) {
                Entry<K,V> e = i.next();
                if (key.equals(e.getKey()))
                    return true;
            }
        }
        return false;
    }

    
    public V get(Object key) {
        Iterator<Entry<K,V>> i = entrySet().iterator();
        if (key==null) {
            while (i.hasNext()) {
                Entry<K,V> e = i.next();
                if (e.getKey()==null)
                    return e.getValue();
            }
        } else {
            while (i.hasNext()) {
                Entry<K,V> e = i.next();
                if (key.equals(e.getKey()))
                    return e.getValue();
            }
        }
        return null;
    }


    // Modification Operations

    
    public V put(K key, V value) {
        throw new UnsupportedOperationException();
    }

    
    public V remove(Object key) {
        Iterator<Entry<K,V>> i = entrySet().iterator();
        Entry<K,V> correctEntry = null;
        if (key==null) {
            while (correctEntry==null && i.hasNext()) {
                Entry<K,V> e = i.next();
                if (e.getKey()==null)
                    correctEntry = e;
            }
        } else {
            while (correctEntry==null && i.hasNext()) {
                Entry<K,V> e = i.next();
                if (key.equals(e.getKey()))
                    correctEntry = e;
            }
        }

        V oldValue = null;
        if (correctEntry !=null) {
            oldValue = correctEntry.getValue();
            i.remove();
        }
        return oldValue;
    }


    // Bulk Operations

    
    public void putAll(Map<? extends K, ? extends V> m) {
        for (Entry<? extends K, ? extends V> e : m.entrySet())
            put(e.getKey(), e.getValue());
    }

    
    public void clear() {
        entrySet().clear();
    }


    // Views

    
    transient Set<K> keySet;
    transient Collection<V> values;

    
    public Set<K> keySet() {
        Set<K> ks = keySet;
        if (ks == null) {
            ks = new AbstractSet<K>() {
                public Iterator<K> iterator() {
                    return new Iterator<K>() {
                        private Iterator<Entry<K,V>> i = entrySet().iterator();

                        public boolean hasNext() {
                            return i.hasNext();
                        }

                        public K next() {
                            return i.next().getKey();
                        }

                        public void remove() {
                            i.remove();
                        }
                    };
                }

                public int size() {
                    return AM.this.size();
                }

                public boolean isEmpty() {
                    return AM.this.isEmpty();
                }

                public void clear() {
                    AM.this.clear();
                }

                public boolean contains(Object k) {
                    return AM.this.containsKey(k);
                }
            };
            keySet = ks;
        }
        return ks;
    }

    
    public Collection<V> values() {
        Collection<V> vals = values;
        if (vals == null) {
            vals = new AbstractCollection<V>() {
                public Iterator<V> iterator() {
                    return new Iterator<V>() {
                        private Iterator<Entry<K,V>> i = entrySet().iterator();

                        public boolean hasNext() {
                            return i.hasNext();
                        }

                        public V next() {
                            return i.next().getValue();
                        }

                        public void remove() {
                            i.remove();
                        }
                    };
                }

                public int size() {
                    return AM.this.size();
                }

                public boolean isEmpty() {
                    return AM.this.isEmpty();
                }

                public void clear() {
                    AM.this.clear();
                }

                public boolean contains(Object v) {
                    return AM.this.containsValue(v);
                }
            };
            values = vals;
        }
        return vals;
    }

    public abstract Set<Entry<K,V>> entrySet();


    // Comparison and hashing

    
    public boolean equals(Object o) {
        if (o == this)
            return true;

        if (!(o instanceof Map<?, ?> m))
            return false;
        if (m.size() != size())
            return false;

        try {
            for (Entry<K, V> e : entrySet()) {
                K key = e.getKey();
                V value = e.getValue();
                if (value == null) {
                    if (!(m.get(key) == null && m.containsKey(key)))
                        return false;
                } else {
                    if (!value.equals(m.get(key)))
                        return false;
                }
            }
        } catch (ClassCastException unused) {
            return false;
        } catch (NullPointerException unused) {
            return false;
        }

        return true;
    }

    
    public int hashCode() {
        int h = 0;
        for (Entry<K, V> entry : entrySet())
            h += entry.hashCode();
        return h;
    }

    
    public String toString() {
        Iterator<Entry<K,V>> i = entrySet().iterator();
        if (! i.hasNext())
            return "{}";

        StringBuilder sb = new StringBuilder();
        sb.append('{');
        for (;;) {
            Entry<K,V> e = i.next();
            K key = e.getKey();
            V value = e.getValue();
            sb.append(key   == this ? "(this Map)" : key);
            sb.append('=');
            sb.append(value == this ? "(this Map)" : value);
            if (! i.hasNext())
                return sb.append('}').toString();
            sb.append(',').append(' ');
        }
    }

    
    protected Object clone() throws CloneNotSupportedException {
        AM<?,?> result = (AM<?,?>)super.clone();
        result.keySet = null;
        result.values = null;
        return result;
    }

    
    private static boolean eq(Object o1, Object o2) {
        return o1 == null ? o2 == null : o1.equals(o2);
    }

    // Implementation Note: SimpleEntry and SimpleImmutableEntry
    // are distinct unrelated classes, even though they share
    // some code. Since you can't add or subtract final-ness
    // of a field in a subclass, they can't share representations,
    // and the amount of duplicated code is too small to warrant
    // exposing a common abstract class.


    
    public static class SimpleEntry<K,V>
        implements Entry<K,V>, java.io.Serializable
    {
        @java.io.Serial
        private static final long serialVersionUID = -8499721149061103585L;

        @SuppressWarnings("serial") // Conditionally serializable
        private final K key;
        @SuppressWarnings("serial") // Conditionally serializable
        private V value;

        
        public SimpleEntry(K key, V value) {
            this.key   = key;
            this.value = value;
        }

        
        public SimpleEntry(Entry<? extends K, ? extends V> entry) {
            this.key   = entry.getKey();
            this.value = entry.getValue();
        }

        
        public K getKey() {
            return key;
        }

        
        public V getValue() {
            return value;
        }

        
        public V setValue(V value) {
            V oldValue = this.value;
            this.value = value;
            return oldValue;
        }

        
        public boolean equals(Object o) {
            return o instanceof Map.Entry<?, ?> e
                    && eq(key, e.getKey())
                    && eq(value, e.getValue());
        }

        
        public int hashCode() {
            return (key   == null ? 0 :   key.hashCode()) ^
                   (value == null ? 0 : value.hashCode());
        }

        
        public String toString() {
            return key + "=" + value;
        }

    }

    
    public static class SimpleImmutableEntry<K,V>
        implements Entry<K,V>, java.io.Serializable
    {
        @java.io.Serial
        private static final long serialVersionUID = 7138329143949025153L;

        @SuppressWarnings("serial") // Not statically typed as Serializable
        private final K key;
        @SuppressWarnings("serial") // Not statically typed as Serializable
        private final V value;

        
        public SimpleImmutableEntry(K key, V value) {
            this.key   = key;
            this.value = value;
        }

        
        public SimpleImmutableEntry(Entry<? extends K, ? extends V> entry) {
            this.key   = entry.getKey();
            this.value = entry.getValue();
        }

        
        public K getKey() {
            return key;
        }

        
        public V getValue() {
            return value;
        }

        
        public V setValue(V value) {
            throw new UnsupportedOperationException();
        }

        
        public boolean equals(Object o) {
            return o instanceof Map.Entry<?, ?> e
                    && eq(key, e.getKey())
                    && eq(value, e.getValue());
        }

        
        public int hashCode() {
            return (key   == null ? 0 :   key.hashCode()) ^
                   (value == null ? 0 : value.hashCode());
        }

        
        public String toString() {
            return key + "=" + value;
        }

    }

}
